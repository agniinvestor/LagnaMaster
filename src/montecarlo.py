"""Monte Carlo birth time sensitivity analysis (Session 11)."""
from __future__ import annotations
import random,statistics
from concurrent.futures import ProcessPoolExecutor,as_completed
from dataclasses import dataclass
from datetime import date
from typing import Optional
@dataclass
class HouseSensitivity:
    house:int;mean_score:float;std_score:float;min_score:float
    max_score:float;score_range:float;rating_mode:str;stable:bool
@dataclass
class SensitivityReport:
    n_samples:int;birth_time_window_minutes:int;lagna_stability:float
    dominant_lagna:str;dasha_stability:float;dominant_md_lord:str;houses:dict
def _worker(args):
    y,mo,d,h,lat,lon,tz,ay,ep,bdi=args
    from src.ephemeris import compute_chart; from src.scoring import score_chart
    c=compute_chart(year=y,month=mo,day=d,hour=h,lat=lat,lon=lon,tz_offset=tz,ayanamsha=ay,ephe_path=ep)
    s=score_chart(c); ml="N/A"
    if bdi:
        try:
            from src.calculations.vimshottari_dasa import compute_vimshottari_dasa,current_dasha
            from datetime import date as _d
            ds=compute_vimshottari_dasa(c,_d.fromisoformat(bdi)); md,_=current_dasha(ds); ml=md.lord
        except: pass
    return{"lagna_sign":c.lagna_sign,"md_lord":ml,
           "house_scores":{h:hs.final_score for h,hs in s.houses.items()},
           "house_ratings":{h:hs.rating for h,hs in s.houses.items()}}
def compute_sensitivity(year,month,day,hour,lat,lon,tz_offset=5.5,ayanamsha="lahiri",
    ephe_path=None,n_samples=100,window_minutes=30,seed=None,birth_date=None,max_workers=4):
    rng=random.Random(seed); wh=window_minutes/60.0
    sh=[max(0.0,min(23.9999,hour+rng.uniform(-wh,wh))) for _ in range(n_samples)]
    bdi=birth_date.isoformat() if birth_date else None
    al=[(year,month,day,h,lat,lon,tz_offset,ayanamsha,ephe_path,bdi) for h in sh]
    orig=_worker((year,month,day,hour,lat,lon,tz_offset,ayanamsha,ephe_path,bdi)); results=[]
    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        for f in as_completed([ex.submit(_worker,a) for a in al]): results.append(f.result())
    lc={}
    for r in results: lc[r["lagna_sign"]]=lc.get(r["lagna_sign"],0)+1
    dl=max(lc,key=lambda k:lc[k]); n=len(results); ls=lc.get(orig["lagna_sign"],0)/n if n else 1.0
    mc={}
    for r in results: mc[r["md_lord"]]=mc.get(r["md_lord"],0)+1
    dm=max(mc,key=lambda k:mc[k]) if mc else "N/A"
    ds=mc.get(orig["md_lord"],0)/n if birth_date and orig["md_lord"]!="N/A" and n else 1.0
    houses={}
    for h in range(1,13):
        hs=[r["house_scores"].get(h,0.0) for r in results]; hr=[r["house_ratings"].get(h,"?") for r in results]
        hn=len(hs); mean=sum(hs)/hn if hn else 0.0; std=statistics.stdev(hs) if hn>1 else 0.0
        mn=min(hs) if hs else 0.0; mx=max(hs) if hs else 0.0
        houses[h]=HouseSensitivity(h,round(mean,4),round(std,4),round(mn,4),round(mx,4),round(mx-mn,4),max(set(hr),key=hr.count) if hr else "?",std<0.5)
    return SensitivityReport(n_samples,window_minutes,round(ls,4),dl,round(ds,4),dm,houses)
