# coding=utf-8
import sys
import urllib2

class Updater(object):

    # 可用hosts源地址列表
    available_hosts_list = [
        ('racaljk', 'https://raw.githubusercontent.com/racaljk/hosts/master/hosts'),
        ('ACXNX', 'https://raw.githubusercontent.com/ACXNX/Hosts-Update/master/hosts'),
        ('blog.my-eclipse.cn', 'http://blog.my-eclipse.cn/hosts.txt')
    ]
    HOSTS_FILE = {
        'windows': 'C:\Windows\System32\drivers\etc\hosts',
        'linux': '/etc/hosts',
    }

    # 兼容 windows 和 linux 平台，其他平台暂时忽略
    os = 'windows' if sys.platform.startswith('win') else 'linux'
    hosts_file = HOSTS_FILE['windows']

    def __init__(self):
        self.hosts_file = self.HOSTS_FILE[self.os]


    def display_options(self):
        """显示可用的 hosts 源"""

        selection = '0'

        while selection == '0' or selection == '':
            print '-'*32 + ' Available Hosts Source ' + '-'*32 + '\n'
            for index, hosts in enumerate(self.available_hosts_list):
                print '[{index}] {alias:<18} ({src})'.format(index=index+1, alias=hosts[0], src=hosts[1])
                # print '[' + str(index+1) + '] ' + hosts[0] + ' (' + hosts[1] + ')'
            print '\n[-] Select a resource. (press "Ctrl+C" to exit.):'
            selection = raw_input('[>] ')
        else:
            index = int(selection) - 1
            if self.available_hosts_list[index]:
                hosts_url = self.available_hosts_list[index][1]
                print '\n'
                self.update(hosts_url)
            else:
                print 'Could not found the hosts url in hosts list. Program will be exit.'
                sys.exit(1)


    def update(self, hosts_url):
        """更新操作"""
        content = self.__fetch_hosts_content(hosts_url)
        if content:
            print '[*] Updating....'
            with open(self.hosts_file, 'w') as file:
                file.write(content)
            print '[*] Completed successfully!'
        else:
            print '[#] No content. Update finished.'
            sys.exit(0)


    def __fetch_hosts_content(self, url):
        """请求远程 hosts 内容"""

        content = None
        try:
            print '[*] Connecting {url}'.format(url=url)
            resp = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            if e.code == 404:
                print '[#] Error 404: Resource not found.'
                print '[#] Program exit.'
                sys.exit(0)
        else:
            status_code = resp.getcode()
            if status_code == 200:
                print '[*] Downloading....'
                content = resp.read()
            elif status_code == 404:
                print '[#] Error 404: Resource not found.'
                print '[#] Program exit.'
                sys.exit(0)
            else:
                print '[#] Error {code}'.format(code=status_code)
                print '[#] Program exit.'
                sys.exit(0)

        return content


    def start(self):
        """启动程序"""

        self.display_options()


if __name__ == '__main__':
    updater = Updater()
    updater.start()
