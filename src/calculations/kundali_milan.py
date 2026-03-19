"""Kundali Milan — Ashtakoot 36-point compatibility engine (Session 12)."""
from __future__ import annotations
from dataclasses import dataclass

_SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
          "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
NAKSHATRAS = [
    "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra",
    "Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni",
    "Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha",
    "Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana",
    "Dhanishtha","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati",
]
_VARNA={"Cancer":0,"Scorpio":0,"Pisces":0,"Aries":1,"Leo":1,"Sagittarius":1,
        "Taurus":2,"Virgo":2,"Capricorn":2,"Gemini":3,"Libra":3,"Aquarius":3}
_VARNA_NAMES={0:"Brahmin",1:"Kshatriya",2:"Vaishya",3:"Shudra"}
_VASHYA_GROUP={"Aries":"quadruped","Taurus":"quadruped","Gemini":"human",
    "Cancer":"jalachara","Leo":"vanachara","Virgo":"human","Libra":"human",
    "Scorpio":"keeta","Sagittarius":"quadruped_human",
    "Capricorn":"jalachara_quadruped","Aquarius":"human","Pisces":"jalachara"}
_VASHYA_DOM={"quadruped":["quadruped","jalachara"],"human":["quadruped","quadruped_human"],
    "jalachara":["jalachara","keeta"],"vanachara":["quadruped"],"keeta":[],
    "quadruped_human":["quadruped","human"],"jalachara_quadruped":["jalachara","quadruped"]}
_TARA_SCORES={1:3,2:3,3:0,4:3,5:0,6:3,7:0,8:3,9:3}
_YONI=["horse","elephant","goat","serpent","dog","cat","cat","goat","cat",
       "rat","rat","cow","buffalo","tiger","buffalo","tiger","deer","deer",
       "dog","monkey","mongoose","monkey","lion","horse","lion","cow","elephant"]
_YONI_ENEMIES={frozenset({"horse","buffalo"}),frozenset({"elephant","lion"}),
    frozenset({"goat","monkey"}),frozenset({"serpent","mongoose"}),
    frozenset({"dog","deer"}),frozenset({"cat","rat"}),frozenset({"tiger","cow"})}
_SIGN_LORD={"Aries":"Mars","Taurus":"Venus","Gemini":"Mercury","Cancer":"Moon",
    "Leo":"Sun","Virgo":"Mercury","Libra":"Venus","Scorpio":"Mars",
    "Sagittarius":"Jupiter","Capricorn":"Saturn","Aquarius":"Saturn","Pisces":"Jupiter"}
_NAISARGIKA={"Sun":{"Moon":"F","Mars":"F","Jupiter":"F","Venus":"E","Saturn":"E","Mercury":"N"},
    "Moon":{"Sun":"F","Mars":"N","Jupiter":"F","Venus":"F","Saturn":"N","Mercury":"F"},
    "Mars":{"Sun":"F","Moon":"F","Jupiter":"F","Venus":"N","Saturn":"N","Mercury":"E"},
    "Mercury":{"Sun":"F","Moon":"N","Mars":"N","Jupiter":"N","Venus":"F","Saturn":"F"},
    "Jupiter":{"Sun":"F","Moon":"F","Mars":"F","Mercury":"E","Venus":"E","Saturn":"N"},
    "Venus":{"Sun":"E","Moon":"N","Mars":"N","Mercury":"F","Jupiter":"N","Saturn":"F"},
    "Saturn":{"Sun":"E","Moon":"E","Mars":"N","Mercury":"F","Jupiter":"N","Venus":"F"}}
_GANA=["Deva","Manava","Rakshasa","Deva","Deva","Manava","Deva","Deva","Rakshasa",
       "Rakshasa","Manava","Manava","Deva","Rakshasa","Deva","Rakshasa","Deva","Rakshasa",
       "Rakshasa","Manava","Manava","Deva","Rakshasa","Rakshasa","Manava","Deva","Deva"]
_GANA_TABLE={("Deva","Deva"):6.0,("Deva","Manava"):6.0,("Deva","Rakshasa"):0.0,
    ("Manava","Deva"):5.0,("Manava","Manava"):6.0,("Manava","Rakshasa"):0.0,
    ("Rakshasa","Deva"):1.0,("Rakshasa","Manava"):0.0,("Rakshasa","Rakshasa"):6.0}
_NADI=["Aadi","Madhya","Antya","Antya","Madhya","Aadi","Aadi","Madhya","Antya",
       "Antya","Madhya","Aadi","Aadi","Madhya","Antya","Antya","Madhya","Aadi",
       "Aadi","Madhya","Antya","Antya","Madhya","Aadi","Aadi","Madhya","Antya"]
_MANGAL_HOUSES={1,2,4,7,8,12}

def _nak_idx(lon:float)->int: return min(int(lon/(360/27)),26)
def _whole_sign_house(p:int,r:int)->int: return (p-r)%12+1

def _varna_score(ms:str,fs:str)->float:
    return 1.0 if _VARNA.get(ms,3)<=_VARNA.get(fs,3) else 0.0
def _vashya_score(ms:str,fs:str)->float:
    mg=_VASHYA_GROUP.get(ms,"human"); fg=_VASHYA_GROUP.get(fs,"human")
    if mg==fg: return 2.0
    if fg in _VASHYA_DOM.get(mg,[]): return 2.0
    if mg in _VASHYA_DOM.get(fg,[]): return 1.0
    return 0.0
def _tara_score(m:int,f:int)->float:
    fwd=((f-m)%27)+1; rev=((m-f)%27)+1
    return min(3.0,(_TARA_SCORES[((fwd-1)%9)+1]+_TARA_SCORES[((rev-1)%9)+1])/2.0)
def _yoni_score(m:int,f:int)->float:
    my=_YONI[m]; fy=_YONI[f]
    if my==fy: return 4.0
    return 0.0 if frozenset({my,fy}) in _YONI_ENEMIES else 2.0
def _graha_maitri_score(ms:str,fs:str)->float:
    ml=_SIGN_LORD.get(ms,"Mercury"); fl=_SIGN_LORD.get(fs,"Mercury")
    if ml==fl: return 5.0
    mf=_NAISARGIKA.get(ml,{}).get(fl,"N"); fm=_NAISARGIKA.get(fl,{}).get(ml,"N")
    if mf=="F" and fm=="F": return 5.0
    if mf=="F" or fm=="F": return 4.0
    if mf=="N" and fm=="N": return 3.0
    if mf=="E" and fm=="E": return 0.0
    return 1.0
def _gana_score(m:int,f:int)->float:
    return _GANA_TABLE.get((_GANA[m],_GANA[f]),0.0)
def _bhakut_score(m:int,f:int)->float:
    m2f=(f-m)%12+1; f2m=(m-f)%12+1
    return 0.0 if m2f in(5,6,8,9) or f2m in(5,6,8,9) else 7.0
def _nadi_score(m:int,f:int)->float:
    return 0.0 if _NADI[m]==_NADI[f] else 8.0
def _bhakut_note(m:int,f:int)->str:
    m2f=(f-m)%12+1; f2m=(m-f)%12+1
    if m2f in(6,8) or f2m in(6,8): return "6/8 Bhakut Dosha"
    if m2f in(5,9) or f2m in(5,9): return "5/9 Bhakut Dosha"
    return ""

def has_mangal_dosha(chart)->bool:
    mars_si=chart.planets["Mars"].sign_index
    for ref in (chart.lagna_sign_index,
                chart.planets["Moon"].sign_index,
                chart.planets["Venus"].sign_index):
        if _whole_sign_house(mars_si,ref) in _MANGAL_HOUSES:
            return True
    return False

def _mangal_dosha_cancelled(cm,cf)->bool:
    return has_mangal_dosha(cm) and has_mangal_dosha(cf)

def _grade(s:float)->str:
    return "Excellent" if s>=28 else "Good" if s>=18 else "Weak"

@dataclass
class KootaScore:
    name:str; max_score:float; score:float
    male_value:str; female_value:str; note:str=""
    @property
    def percentage(self)->float:
        return self.score/self.max_score*100 if self.max_score else 0.0
    @property
    def is_dosha(self)->bool:
        return self.score==0.0 and self.max_score>0

@dataclass
class KundaliMilanResult:
    total_score:float; max_score:float; percentage:float; grade:str
    kootas:dict
    mangal_dosha_male:bool; mangal_dosha_female:bool; dosha_cancelled:bool
    nadi_dosha:bool; bhakut_dosha:bool; critical_doshas:list

def compute_kundali_milan(chart_male,chart_female)->KundaliMilanResult:
    m_moon_lon=chart_male.planets["Moon"].longitude
    f_moon_lon=chart_female.planets["Moon"].longitude
    m_nak=_nak_idx(m_moon_lon); f_nak=_nak_idx(f_moon_lon)
    m_moon_sign=chart_male.planets["Moon"].sign
    f_moon_sign=chart_female.planets["Moon"].sign
    m_moon_si=chart_male.planets["Moon"].sign_index
    f_moon_si=chart_female.planets["Moon"].sign_index
    v=_varna_score(m_moon_sign,f_moon_sign)
    va=_vashya_score(m_moon_sign,f_moon_sign)
    t=_tara_score(m_nak,f_nak)
    y=_yoni_score(m_nak,f_nak)
    gm=_graha_maitri_score(m_moon_sign,f_moon_sign)
    g=_gana_score(m_nak,f_nak)
    b=_bhakut_score(m_moon_si,f_moon_si)
    n=_nadi_score(m_nak,f_nak)
    total=v+va+t+y+gm+g+b+n
    kootas={
        "Varna":KootaScore("Varna",1.0,v,_VARNA_NAMES.get(_VARNA.get(m_moon_sign,3),"?"),_VARNA_NAMES.get(_VARNA.get(f_moon_sign,3),"?")),
        "Vashya":KootaScore("Vashya",2.0,va,_VASHYA_GROUP.get(m_moon_sign,"?"),_VASHYA_GROUP.get(f_moon_sign,"?")),
        "Tara":KootaScore("Tara",3.0,t,NAKSHATRAS[m_nak],NAKSHATRAS[f_nak]),
        "Yoni":KootaScore("Yoni",4.0,y,_YONI[m_nak],_YONI[f_nak]),
        "Graha Maitri":KootaScore("Graha Maitri",5.0,gm,_SIGN_LORD.get(m_moon_sign,"?"),_SIGN_LORD.get(f_moon_sign,"?")),
        "Gana":KootaScore("Gana",6.0,g,_GANA[m_nak],_GANA[f_nak]),
        "Bhakut":KootaScore("Bhakut",7.0,b,m_moon_sign,f_moon_sign,_bhakut_note(m_moon_si,f_moon_si)),
        "Nadi":KootaScore("Nadi",8.0,n,_NADI[m_nak],_NADI[f_nak],"Nadi Dosha" if n==0.0 else ""),
    }
    nadi_d=n==0.0; bhakut_d=b==0.0
    m_m=has_mangal_dosha(chart_male); f_m=has_mangal_dosha(chart_female)
    cancelled=_mangal_dosha_cancelled(chart_male,chart_female)
    critical=[]
    if nadi_d: critical.append("Nadi Dosha")
    if bhakut_d: critical.append("Bhakut Dosha")
    if m_m and not cancelled: critical.append("Mangal Dosha (Male)")
    if f_m and not cancelled: critical.append("Mangal Dosha (Female)")
    return KundaliMilanResult(
        total_score=round(total,2),max_score=36.0,
        percentage=round(total/36*100,1),grade=_grade(total),
        kootas=kootas,mangal_dosha_male=m_m,mangal_dosha_female=f_m,
        dosha_cancelled=cancelled,nadi_dosha=nadi_d,bhakut_dosha=bhakut_d,
        critical_doshas=critical,
    )
