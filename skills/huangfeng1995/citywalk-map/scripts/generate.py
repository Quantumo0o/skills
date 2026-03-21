#!/usr/bin/env python3
"""
Citywalk Map Generator
Usage: python3 generate.py "路线标题" "lat1,lon1,name1,desc1|lat2,lon2,name2,desc2|..."
       COLOR=hex python3 generate.py ...  (设置主题色，默认 #e94560)
Output: /tmp/citywalk_map.html

依赖: requests (pip install requests)
"""
import sys, os, json, math, subprocess

def get_osrm_route(waypoints):
    """调用 OSRM 步行路由 API 获取真实路线距离、时间和几何（通过 curl）"""
    total_distance = 0
    total_duration = 0
    full_route_coords = []

    for i in range(len(waypoints) - 1):
        p1 = waypoints[i]
        p2 = waypoints[i + 1]
        lon1, lat1 = p1['lon'], p1['lat']
        lon2, lat2 = p2['lon'], p2['lat']

        url = f"https://router.project-osrm.org/route/v1/foot/{lon1},{lat1};{lon2},{lat2}"
        cmd = ['curl', '-s', '--max-time', '10', url, '-G', '--data-urlencode', 'overview=full', '--data-urlencode', 'geometries=geojson']
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=12)
            data = json.loads(result.stdout)
            if data.get('code') == 'Ok':
                route = data['routes'][0]
                total_distance += route['distance']
                # OSRM 距离正确，但 duration 可能是骑行速度，改用步行速度 5km/h
                total_duration += route['distance'] / 1.39
                coords = route['geometry']['coordinates']
                full_route_coords.extend([[c[1], c[0]] for c in coords])
            else:
                raise ValueError(f"OSRM error: {data.get('code')}")
        except Exception as e:
            print(f"OSRM error: {e}, using fallback", file=sys.stderr)
            dlat = (lat2 - lat1) * 111000
            dlon = (lon2 - lon1) * 111000 * math.cos(math.radians(lat1))
            dist = math.sqrt(dlat**2 + dlon**2)
            total_distance += dist * 1.3
            total_duration += dist * 1.3 / 1.1
            full_route_coords.append([lat1, lon1])
            full_route_coords.append([lat2, lon2])

    return total_distance, total_duration, full_route_coords

ACCENT = os.environ.get('COLOR', '#e94560')

def darken(hex_color):
    if hex_color.startswith('#'):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        f = 0.75
        return '#{:02x}{:02x}{:02x}'.format(int(r*f), int(g*f), int(b*f))
    return ACCENT

def fmt_d(m):
    return f"{m/1000:.1f}km" if m >= 1000 else f"{int(m)}m"

def fmt_t(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    return f"{h}h{m}m" if h > 0 else f"{m}min"

def fmt_d_hori(m):
    return f"{m/1000:.1f}km" if m >= 1000 else f"{int(m)}m"

def fmt_t_hori(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    return f"{h}h{m}m" if h > 0 else f"{m}min"

if len(sys.argv) < 3:
    print(__doc__)
    sys.exit(1)

title = sys.argv[1]
parts = sys.argv[2].split('|')
waypoints = []
for i, p in enumerate(parts):
    s = p.split(',')
    waypoints.append({
        'num': str(i+1),
        'lat': float(s[0].strip()),
        'lon': float(s[1].strip()),
        'name': s[2].strip() if len(s) > 2 else f"点{i+1}",
        'desc': s[3].strip() if len(s) > 3 else ''
    })

clat = sum(w['lat'] for w in waypoints) / len(waypoints)
clon = sum(w['lon'] for w in waypoints) / len(waypoints)

print(f"正在查询 OSRM 步行路由 ({len(waypoints)} 个站点)...")
td, walk_sec, route_coords = get_osrm_route(waypoints)

# 每站停留时间：30分钟
visit_sec = len(waypoints) * 30 * 60
dm = walk_sec + visit_sec

route_html_lines = []
for i, w in enumerate(waypoints):
    cls = 's1' if i == 0 else ('sN' if i == len(waypoints) - 1 else 'sx')
    route_html_lines.append(f'          <li><span class="route-num {cls}">{w["num"]}</span>{w["name"]}</li>')
route_html = '\n'.join(route_html_lines)

tips = ['建议提前出发，合理安排时间', '穿着舒适的步行鞋', '携带水瓶和防晒用品', '注意安全，遵守当地规定']
tips_html = '\n'.join(f'          <li>{t}</li>' for t in tips)

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>{title}</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif;
  background: {accent};
  min-height: 100vh;
  padding: 16px 0;
  display: flex;
  align-items: flex-start;
}}
.card {{
  width: 100%;
  max-width: 100%;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
}}
.header {{
  background: linear-gradient(135deg, {accent} 0%, {accent_dark} 100%);
  padding: 18px 20px 16px;
  color: white;
}}
.header .tag {{
  display: inline-block;
  background: rgba(255,255,255,0.2);
  border-radius: 10px;
  padding: 4px 12px;
  font-size: 10px;
  letter-spacing: 1px;
  margin-bottom: 6px;
}}
.header h1 {{ font-size: 22px; font-weight: 700; margin-bottom: 4px; }}
.header p {{ font-size: 13px; opacity: 0.85; }}
#map {{ width: 100%; height: 520px; }}
.info {{ padding: 16px 18px; }}
.stats {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 14px;
}}
.stat {{
  background: #f5f7fa;
  border-radius: 10px;
  padding: 10px 6px;
  text-align: center;
}}
.stat .num {{ font-size: 20px; font-weight: 700; color: {accent}; }}
.stat .label {{ font-size: 11px; color: #888; margin-top: 3px; }}
.bottom {{ display: flex; gap: 12px; }}
.bottom-left {{ flex: 1.5; background: #f5f7fa; border-radius: 12px; padding: 12px 14px; }}
.bottom-right {{ flex: 1; background: #f5f7fa; border-radius: 12px; padding: 12px 14px; }}
.section-title {{ font-size: 11px; color: #888; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 8px; font-weight: 600; }}
.route-list {{ list-style: none; padding: 0; margin: 0; }}
.route-list li {{ display: flex; align-items: center; gap: 10px; padding: 7px 0; font-size: 13px; color: #333; border-bottom: 1px solid #eee; }}
.route-list li:last-child {{ border-bottom: none; }}
.route-num {{ width: 22px; height: 22px; border-radius: 50%; font-size: 10px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: white; }}
.route-num.s1 {{ background: {accent}; }}
.route-num.sx {{ background: #ff9f43; }}
.route-num.sN {{ background: #10b981; }}
.tips {{ list-style: none; padding: 0; margin: 0; }}
.tips li {{ font-size: 12px; color: #333; line-height: 1.6; padding: 6px 0; border-bottom: 1px solid #eee; }}
.tips li:last-child {{ border-bottom: none; }}
.popup-title {{ font-size: 14px; font-weight: 700; color: #222; margin-bottom: 4px; }}
.popup-desc {{ font-size: 12px; color: #666; }}
.popup-num {{ display: inline-block; width: 20px; height: 20px; background: {accent}; color: white; border-radius: 50%; text-align: center; line-height: 20px; font-size: 10px; font-weight: 700; margin-right: 6px; }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <div class="tag">🚶 CITYWALK</div>
    <h1>{title}</h1>
    <p>{subtitle}</p>
  </div>
  <div id="map"></div>
  <div class="info">
    <div class="stats">
      <div class="stat"><div class="num">{dist}</div><div class="label">步行距离</div></div>
      <div class="stat"><div class="num">{dur}</div><div class="label">游览时长</div></div>
      <div class="stat"><div class="num">{n}站</div><div class="label">途经景点</div></div>
      <div class="stat"><div class="num">{walk}</div><div class="label">纯步行</div></div>
    </div>
    <div class="bottom">
      <div class="bottom-left">
        <div class="section-title">途经景点</div>
        <ul class="route-list">
{route_html}
        </ul>
      </div>
      <div class="bottom-right">
        <div class="section-title">实用贴士</div>
        <ul class="tips">
{tips_html}
        </ul>
      </div>
    </div>
  </div>
</div>
<script>
var waypoints = {waypoints_json};
var routeCoords = {route_json};
var map = L.map('map', {{zoomControl:true, scrollWheelZoom:false}}).setView([{center_lat},{center_lon}], 14);
L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{maxZoom:19, attribution:'© OpenStreetMap'}}).addTo(map);
L.polyline(routeCoords, {{color:'{accent}', weight:5, opacity:0.85, dashArray:'10, 5'}}).addTo(map);
var ds = Math.max(1, Math.floor(routeCoords.length/12));
for(var i=0;i<routeCoords.length-1;i+=ds){{
  L.circleMarker(routeCoords[i], {{radius:4, color:'{accent}', fillColor:'{accent}', fillOpacity:0.9}}).addTo(map);
}}
waypoints.forEach(function(wp){{
  var last = waypoints[waypoints.length-1].num;
  var color = wp.num==='1'?'{accent}':(wp.num===last?'#10b981':'#ff9f43');
  L.circleMarker([wp.lat,wp.lon], {{radius:10, color:'white', weight:3, fillColor:color, fillOpacity:1}})
    .addTo(map).bindPopup('<div class="popup-title"><span class="popup-num" style="background:'+color+'">'+wp.num+'</span>'+wp.name+'</div><div class="popup-desc">'+(wp.desc||'')+'</div>');
  var lbl = L.divIcon({{html:'<div style="background:white;padding:3px 8px;border-radius:8px;font-size:11px;font-weight:600;box-shadow:0 2px 8px rgba(0,0,0,0.2);white-space:nowrap;border-left:3px solid '+color+';">'+wp.name+'</div>', className:'', iconSize:[0,0], iconAnchor:[0,0]}});
  L.marker([wp.lat,wp.lon], {{icon:lbl}}).addTo(map);
}});
var b = L.latLngBounds(waypoints.map(function(wp){{return[wp.lat,wp.lon];}}));
map.fitBounds(b, {{padding:[10,10]}});
var n=L.control({{position:'bottomleft'}});n.onAdd=function(){{
  var d=L.DomUtil.create('div');
  d.innerHTML='<div style="background:white;padding:6px 8px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.2);text-align:center;font-size:10px;font-weight:700;color:#333;">⬆ N</div>';
  return d;
}};n.addTo(map);
</script>
</body>
</html>
"""

total_dur_str = fmt_t(dm)
walk_str = fmt_t(walk_sec)

html = HTML.format(
    title=title,
    subtitle=f"{len(waypoints)}大景点 · 全程{fmt_d(td)} · 游览约{total_dur_str}",
    accent=ACCENT,
    accent_dark=darken(ACCENT),
    waypoints_json=json.dumps(waypoints),
    route_json=json.dumps(route_coords),
    center_lat=clat,
    center_lon=clon,
    dist=fmt_d(td),
    dur=total_dur_str,
    n=len(waypoints),
    walk=walk_str,
    route_html=route_html,
    tips_html=tips_html,
)

with open('/tmp/citywalk_map.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f"OK: {title} | accent={ACCENT} | {len(waypoints)} pts | {fmt_d(td)} | 步行{fmt_t(walk_sec)} | 游览{total_dur_str}")
