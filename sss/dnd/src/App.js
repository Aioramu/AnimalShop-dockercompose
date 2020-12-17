import React, {useEffect,useState} from 'react';
import {DragDropContext, Droppable, Draggable} from 'react-beautiful-dnd';
import { v4 as uuid } from 'uuid';
import './App.css'
//hard coded not worked:D
var petsProds = [
  {
    id: '0',
    name: 'Billy',
    price:5000,

  },
  {
    id: '1',
    name: 'jojo',
    price:1000,

  },
  {
    id: '2',
    name: 'kimmy',
    price:4000,

  },
  {
    id: '3',
    name: 'bobby',
    price:5000,

  },
  {
    id: '4',
    name: 'molly',
    price:10000,

  }
]

const columnsAll =
  {
    [uuid()]: {
      name: 'Выбирай',
      items: petsProds
    },
    [uuid()]: {
      name: 'Перетаскивай',
      items: []
    }
  }

const onDragEnd = (result, columns, setColumns) => {
  if(!result.destination) return;
  const {source, destination} = result;
  if(source.droppableId !== destination.droppableId) {
    const sourceColumn = columns[source.droppableId];
    const destinationColumn = columns[destination.droppableId];
    const sourceItems = [...sourceColumn.items];
    const destinationItems = [...destinationColumn.items];
    const [removed] = sourceItems.splice(source.index, 1);
    destinationItems.splice(destination.index, 0, removed);
    setColumns({
      ...columns,
      [source.droppableId]: {
        ...sourceColumn,
        items:sourceItems
      },
      [destination.droppableId]: {
        ...destinationColumn,
        items: destinationItems
      }
    })
  } else {
    const column = columns[source.droppableId];
    const copiedItems = [...column.items]
    const [removed] = copiedItems.splice(source.index, 1);
    copiedItems.splice(destination.index, 0, removed);
    setColumns({
      ...columns,
      [source.droppableId]: {
        ...column,
        items: copiedItems
      }
    })
  }

}

function App() {
    fetch('/all/').then(response=>
    response.json().then(data=>{

      var clone=data;
      console.log("sdas",clone)
    }));

  const [columns, setColumns] = useState(columnsAll);

  return (

    <div className="App" style={{display: 'flex', justifyContent: 'center', height: '100%'}}>
      <DragDropContext onDragEnd={result => onDragEnd(result, columns, setColumns)}>
        {Object.entries(columns).map(([id, column]) => {
          return(
            <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
              <h2>{column.name}</h2>
              <div style={{margin: 5}}>
                <Droppable droppableId={id} key={id}>
                  {(provided, snapshot) => {
                    return(
                      <div {...provided.droppableProps} ref={provided.innerRef} style={{background: snapshot.isDraggingOver ? 'lightblue' : 'lightgrey', padding: 4, width: 250, minHeight:500 }}>
                        {column.items.map((item, index) => {
                          return(
                            <Draggable key={item.id} draggableId={item.id} index={index}>
                              {(provided, snapshot) => {
                                return(
                                  <div ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps} style={{userSelect: 'none', padding: 16, margin: '0 0 8px 0', minHeight: '50px', backgroundColor: snapshot.isDragging ? '#263B4A' : '#456C86', color: 'white', ...provided.draggableProps.style}}>
                                    {item.name}
                                    {item.price}
                                  </div>
                                )
                              }}
                            </Draggable>
                          )
                        })}
                        {provided.placeholder}
                      </div>
                    )
                  }}
                </Droppable>
              </div>
            </div>
          )
        })}
      </DragDropContext>
    </div>
  );
}

export default App;
