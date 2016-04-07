pymunincli
==========

A Python library to access Munin_::

    >>> import munin.client
    >>> client = munin.client.Client(host="localhost")
    >>> client.connect()
    >>> client.list()
    ['apache_accesses', 'apache_processes', 'apache_volume', 'cpu', 'cpuspeed', 'df', 'df_inode', 'entropy', 'exim_mailstats', 'forks', 'fw_packets', 'hddtemp_smartctl', 'if_err_eth0', 'if_err_wlan0', 'if_eth0', 'if_wlan0', 'interrupts', 'irqstats', 'load', 'memory', 'munin_stats', 'nfs4_client', 'nfs_client', 'nfsd', 'nfsd4', 'ntp_kernel_err', 'ntp_kernel_pll_freq', 'ntp_kernel_pll_off', 'ntp_offset', 'ntp_states', 'open_files', 'open_inodes', 'proc_pri', 'processes', 'smart_sda', 'swap', 'threads', 'uptime', 'users', 'vmstat']
    >>> client.fetch('uptime')
    {'uptime': 0.32}
    >>> client.config('users')
    {'graph_category': 'system', 'tty': {'draw': 'AREASTACK', 'colour': '00FF00', 'label': 'tty'}, 'pty': {'draw': 'AREASTACK', 'colour': '0000FF', 'label': 'pty'}, 'pts': {'draw': 'AREASTACK', 'colour': '00FFFF', 'label': 'pts'}, 'graph_vlabel': 'Users', 'graph_title': 'Logged in users', 'graph_printf': '%3.0lf', 'X': {'info': 'Users logged in on an X display', 'draw': 'AREASTACK', 'colour': '000000', 'label': 'X displays'}, 'graph_args': '--base 1000 -l 0', 'graph_scale': 'no', 'other': {'info': 'Users logged in by indeterminate method', 'colour': 'FF0000', 'label': 'Other users'}}

.. _Munin: http://munin-monitoring.org/
