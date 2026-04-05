#!/usr/bin/env python3
"""
FIT文件GCJ-02坐标转WGS-84转换器
"""
import sys
import struct
import math
from pathlib import Path
from fitparse import FitFile
from fitparse.records import Crc

# GCJ-02 转 WGS-84 算法
def gcj02_to_wgs84(lng, lat):
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - 0.00669342162296594323 * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((6378245.0 * (1 - 0.00669342162296594323)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (6378245.0 / sqrtmagic * math.cos(radlat) * math.pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return lng * 2 - mglng, lat * 2 - mglat

def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * math.pi) + 40.0 *
            math.sin(lat / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * math.pi) + 320 *
            math.sin(lat * math.pi / 30.0)) * 2.0 / 3.0
    return ret

def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * math.pi) + 40.0 *
            math.sin(lng / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * math.pi) + 300.0 *
            math.sin(lng / 30.0 * math.pi)) * 2.0 / 3.0
    return ret

def out_of_china(lng, lat):
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)

def get_field_by_name(msg, name):
    """获取指定名称的字段"""
    for field in msg.fields:
        if field.name == name:
            return field
    return None

def convert_fit_file(input_path, output_path):
    """转换FIT文件坐标"""
    # 读取原始文件
    with open(input_path, 'rb') as f:
        data = bytearray(f.read())
    
    # 解析FIT文件获取所有记录
    fitfile = FitFile(input_path)
    
    # 收集所有坐标转换映射 (原始值 -> 新值)
    coord_map = {}
    record_count = 0
    
    for msg in fitfile.get_messages('record'):
        lat_field = get_field_by_name(msg, 'position_lat')
        lon_field = get_field_by_name(msg, 'position_long')
        
        if lat_field and lon_field and lat_field.raw_value is not None and lon_field.raw_value is not None:
            lat_sem = lat_field.raw_value
            lon_sem = lon_field.raw_value
            
            # semicircles to degrees
            lat_deg = lat_sem * (180.0 / 2**31)
            lon_deg = lon_sem * (180.0 / 2**31)
            
            # 转换
            lon_wgs, lat_wgs = gcj02_to_wgs84(lon_deg, lat_deg)
            
            # 转回 semicircles
            lat_sem_new = int(lat_wgs * (2**31 / 180.0))
            lon_sem_new = int(lon_wgs * (2**31 / 180.0))
            
            # 存储映射
            coord_map[(lat_sem, lon_sem)] = (lat_sem_new, lon_sem_new)
            record_count += 1
    
    print(f"总共找到 {record_count} 条记录")
    
    # 直接在二进制数据中搜索替换
    modified = 0
    for (old_lat, old_lon), (new_lat, new_lon) in coord_map.items():
        old_lat_bytes = struct.pack('<i', old_lat)
        old_lon_bytes = struct.pack('<i', old_lon)
        new_lat_bytes = struct.pack('<i', new_lat)
        new_lon_bytes = struct.pack('<i', new_lon)
        
        # 搜索并替换
        pos = 0
        while True:
            pos = data.find(old_lat_bytes, pos)
            if pos == -1:
                break
            # 检查下一个4字节是否是匹配的经度
            if pos + 8 <= len(data) and data[pos+4:pos+8] == old_lon_bytes:
                data[pos:pos+4] = new_lat_bytes
                data[pos+4:pos+8] = new_lon_bytes
                modified += 1
                pos += 8
            else:
                pos += 1
    
    print(f"已修改 {modified} 组坐标")
    
    # 修复CRC
    crc_obj = Crc()
    crc_obj.update(data[:-2])
    new_crc = crc_obj.value
    data[-2] = new_crc & 0xFF
    data[-1] = (new_crc >> 8) & 0xFF
    print(f"CRC已更新: 0x{new_crc:04X}")
    
    # 保存修改后的文件
    with open(output_path, 'wb') as f:
        f.write(data)
    
    print(f"已保存到: {output_path}")
    return record_count, modified

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_fit.py <input.fit> <output.fit>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    count, modified = convert_fit_file(input_file, output_file)
    print(f"✅ 转换完成！共 {count} 条坐标记录")
