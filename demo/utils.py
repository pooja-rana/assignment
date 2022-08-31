from django.contrib.sites.shortcuts import get_current_site


def get_domain(request):
    """method for returning current domain from the request"""
    current_site = get_current_site(request).domain
    return current_site
