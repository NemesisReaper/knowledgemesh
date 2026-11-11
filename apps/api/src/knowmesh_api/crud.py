from fastapi import APIRouter,Depends,HTTPException,Query
from .store import store
from .schemas import RecordCreate,SearchRequest
def resource_router(resource):
    r=APIRouter()
    @r.get("")
    def listing(limit:int=Query(50,ge=1,le=100),offset:int=Query(0,ge=0),q:str|None=None):
        return {"items":store.list(resource,limit,offset,q),"limit":limit,"offset":offset}
    @r.post("",status_code=201)
    def create(body:RecordCreate): return store.put(resource,body.model_dump(exclude_none=True),body.id)
    @r.get("/{item_id}")
    def get(item_id:str):
        item=store.get(resource,item_id)
        if item is None: raise HTTPException(404,detail=f"{resource} record not found")
        return item
    @r.delete("/{item_id}",status_code=204)
    def delete(item_id:str):
        if not store.delete(resource,item_id): raise HTTPException(404,detail=f"{resource} record not found")
        return None
    return r
def search_router():
    r=APIRouter()
    @r.post("")
    def search(body:SearchRequest):
        q=body.query.casefold(); hits=[]
        for table in ("bundles","claims","evidence","nodes"):
            for item in store.list(table,limit=10000):
                score=str(item).casefold().count(q)
                if score: hits.append({"resource":table,"id":item["id"],"record":item,"score":score})
        hits.sort(key=lambda x:x["score"],reverse=True)
        return {"query":body.query,"results":hits[:body.limit],"total":len(hits)}
    return r
