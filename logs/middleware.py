import re
import logging
import time
import traceback

from django.conf import settings
from django.http import HttpResponseForbidden
from django.urls import resolve
from django.urls.exceptions import Resolver404

from django_extensions.management.commands import show_urls

from logs.models import RequestLog, VisitorIP


logger = logging.getLogger(__name__)


LOG_IGNORE_PATH_STARTSWITH = [
    '/admin/',
    '/_nested_admin/',
    '/grappelli/',
    '/favicon.ico',
    '/robots.txt',
]

STRIP_INPUT_FIELDS = [
    'csrfmiddlewaretoken',
    'g-recaptcha-response',
    'auth-password',
    'new_password1',
    'new_password2',
    'password1',
    'password2',
]


class LogRequestsMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        self.whitelisted_routes = self.scan_all_routes()

    def __call__(self, request):
        request._start_time = time.monotonic_ns()
        ip_addr = self.client_ip(request)

        request_body = self.request_body(request)
        request_path = request.path

        if not self.log_filter(request):
            logger.warn('ignored: %s', request_path)
            return self.get_response(request)

        visitor_ip = None
        try:        
            visitor_ip, _ = VisitorIP.objects.get_or_create(ip_address=ip_addr)
        except:
            logger.exception("failed to create VisitorIP record")

        if visitor_ip:
            if visitor_ip.blocked:
                logger.warn('ip blocked: %s', request_path)
                return HttpResponseForbidden()

        route = None
        try:
            route = resolve(request_path).route
        except Resolver404 as exc:
            route = exc.args[0]['path']

        if route not in self.whitelisted_routes:
            #TODO: possibly we could block this IP if it hits the web-site too often
            logger.warn('whitelist blocked: %s', request_path)
            return HttpResponseForbidden()

        if visitor_ip:
            visitor_ip.counter += 1
            visitor_ip.save()

        response = self.get_response(request)

        if response.streaming:
            logger.warn('streaming ignored: %s', request_path)
            return response

        try:
            RequestLog.objects.create(
                ip_address=ip_addr,
                user=self.user_email(request),
                method=request.method,
                path=request_path,
                request=request_body,
                status_code=response.status_code,
                exception=getattr(request, '_captured_exception', None) or None,
                duration=(time.monotonic_ns() - request._start_time) / 1000000000.0,
            )
        except:
            logger.exception("failed to create RequestLog record")

        return response

    def process_exception(self, request, exception):
        request._captured_exception = str(exception) + '\n\n' + traceback.format_exc()
        return None

    def log_filter(self, request):
        p = request.path
        if any([p.startswith(ignore_path) for ignore_path in LOG_IGNORE_PATH_STARTSWITH]):
            # skip logging of some specific requests
            return False
        return True

    def user_email(self, request):
        u = getattr(request, 'user', '')
        if u:
            if getattr(u, 'email', ''):
                return u.email
        return u

    def client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        ip = re.sub(r'[^a-zA-Z0-9\.]', '', ip)
        return ip

    def request_body(self, request):
        raw_request_body = ""
        if request.POST:
            try:
                raw_request_body += '\n'.join(['%s=%s' % (k, v) for k, v in request.POST.items() if k not in STRIP_INPUT_FIELDS])
            except Exception as e:
                raw_request_body += str(e)
        if request.GET:
            if raw_request_body:
                raw_request_body += '\n'
            try:
                raw_request_body += '\n'.join(['%s=%s' % (k, v) for k, v in request.GET.items()])
            except Exception as e:
                raw_request_body += str(e)
        return raw_request_body

    def scan_all_routes(self):
        urlconf = __import__(getattr(settings, 'ROOT_URLCONF'), {}, {}, [''])
        routes = set()
        for (_, regex, _) in show_urls.Command().extract_views_from_urlpatterns(urlconf.urlpatterns):
            routes.add(regex)
        return routes
