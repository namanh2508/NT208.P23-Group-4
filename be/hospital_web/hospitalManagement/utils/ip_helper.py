import random
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ip == '127.0.0.1':
        test_ips = ['8.8.8.8', '203.162.4.190', '1.1.1.1', '210.245.31.141']
        return random.choice(test_ips)
    return ip