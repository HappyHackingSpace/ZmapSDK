from zmapsdk import ZMap

zmap = ZMap(zmap_path="/usr/sbin/zmap")

result = zmap.scan(target_port=554, subnets=["192.168.1.0/24"], output_file="test.csv")

print(result)
