import re

def ip_uv(a):
    """
    ip地址匹配
    :param a:
    :return:
    """
    uv = re.search("\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}|-", a).group()
    return uv


def time_uv(a):
    """
    时间匹配
    :param a:
    :return:
    """
    time_u = re.search("(?P<time>\\d{4}:\\d.)", a).group()

    return time_u


def url_pv(a):
    """
    URL匹配
    :param a:
    :return:
    """
    url = re.search("\\w+ /.*HTTP/\\d.\\d", a)
    return url


def facility_uv(a):
    """
    访问设备匹配
    :param a:
    :return:
    """
    facility = re.search("Mozilla/.*", a)
    return facility




ip = []  # IP地址集合
IP = set()
time_pu = []
pu_time = {}
pv_url = []  # URL列表
facility_pv = []    # 访问设备列表
top_pv = {}
top_uv = {}
f = open(file="网站访问日志.txt", mode="r")
for line in f:
    if re.search("^- - - ", line):
        continue
    elif facility_uv(line) is not None:
        ip.append(ip_uv(line))
        IP.add(ip_uv(line))
        pv_url.append(url_pv(line))
        facility_pv.append(str(facility_uv(line).group()))
        time_pu.append(time_uv(line))

facility_u = dict(zip(facility_pv, pv_url))
print("uv总数:", len(IP))
print("pv总数:", len(pv_url))
for k, v in facility_u.items():
    print("设备访问量：%s  访问设备设备名称：%s  " % (len(v), k,))
for top in set(pv_url):
    top_pv[pv_url.count(top)] = top
for e in reversed(sorted(top_pv.keys())[-10:]):
    print("top页面访问量：", e, ":", top_pv[e])
for top_ip in set(ip):
    top_uv[ip.count(top_ip)] = top_ip
for a in reversed(sorted(top_uv.keys())[-10:]):
    print("topIP点击数：", a, ":", top_uv[a])
for uv in reversed(sorted(top_uv.keys())):
    print("每小时的uv数：", uv, ":", top_uv[uv])
for pu in set(time_pu):
    pu_time[time_pu.count(pu)] = pu
for pv in reversed(sorted(pu_time.keys())):
    print("每小时的pv数：", pv, ":", pu_time[pv])


# 计数器，