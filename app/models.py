from dataclasses import dataclass,field
from datetime import datetime
@dataclass
class Item: description:str;quantity:float|None=None;unit:str|None=None;cpv:str|None=None;matched_terms:list[str]=field(default_factory=list)
@dataclass
class Tender:
 id:str;source:str;country:str;title:str;buyer:str='';description:str='';value:float|None=None;currency:str|None=None;deadline:datetime|None=None;published_at:datetime|None=None;status:str='active';source_url:str='';category:str='Other';score:int=0;items:list[Item]=field(default_factory=list)
