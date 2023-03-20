from typing import List

#from typing import Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.todo_lists = {}
app.todo_id_counter = 0
app.todo_id_item_counter = 0


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class ToDoItem(BaseModel):
    id: int
    title: str


class ToDoList(BaseModel):
    id: int
    title: str
    items: List[ToDoItem]




@app.get("/api/todo_lists/")
def show_all_list():
    all_list = list(app.todo_lists.values())
    return all_list

@app.get("/api/todo_lists/{todolist_id}/")
def get_todolist(todolist_id: int):
    if todolist_id not in app.todo_lists:
        raise HTTPException(status_code=404, detail="ToDo list was not found")
    return app.todo_lists[todolist_id]



@app.post("/api/todo_lists/")
def add_a_list(todolist: ToDoList):
    todolist.id = app.todo_id_counter
    app.todo_lists[todolist.id] = todolist
    app.todo_id_counter = app.todo_id_counter + 1
    return todolist

@app.delete("/api/todo_lists/{todolist_id}/")
def delete_todolist(todolist_id: int):
    if todolist_id not in app.todo_lists:
        raise HTTPException(status_code=404, detail="ToDo List was not found")
    del app.todo_lists[todolist_id]

@app.post("/api/todo_lists/{todolist_id}/item/")
def add_todolist_item(todolist_id: int, item: ToDoItem):
    if todolist_id not in app.todo_lists:
        raise HTTPException(status_code=404, detail="ToDo list was not found")
    current_todo_list = app.todo_lists[todolist_id]
    item.id = app.todo_id_item_counter
    current_todo_list.items.append(item)
    app.todo_id_item_counter = app.todo_id_item_counter + 1


@app.delete("/api/todo_lists/{todolist_id}/item/{todoitem_id}/")
def delete_todolist_item(todolist_id: int, todoitem_id: int):
    if todolist_id not in app.todo_lists:
        raise HTTPException(status_code=404, detail="ToDo list was not found")
    current_todo_list = app.todo_lists[todolist_id]
    for item in current_todo_list.items:
        if item.id == todoitem_id:
            current_todo_list.items.remove(item)
            break



if __name__ == "__main__":
    uvicorn.run("todo-service:app", port=8080, host="0.0.0.0") #change to 127.0.0.1 in browser
    #uvicorn.run("todo-service:app", port=8080, host="10.9.8.8")

