import React from "react";
import axios from "axios";
import api from "./api";

export default function Chatbot() {
  // Tenemos un state que define el estado del chat. El state es business por default. Dependiendo del state cambia la configuración de botones. El state también define el mensaje default que se enseña al usuario. Los botones hacen trigger a un api call que actualiza el state. Hay ciertos botones que triggerean un textbox que cuando se manda ya se ejecuta el api call. Cuando se pica un botón o se manda un mensaje, se despliega como mensaje. Cuando llega el response, se despliega como mensaje, se cambia de state y se mandan los nuevos mensajes. Si el usuario no responde al primer mensaje, no contamos válida la interacción. Intentaré generar la lógica de programación yo solo, sin usar ningún tutorial.

  // Primero crearé un state que guarde el chat session id, que se pedirá al backend cuando el usuario mande el primer mensaje.
  const [sessionId, setSessionId] = React.useState({ sessionId: null });

  // Luego crearé un state que mantenga updateado el state del  chat
  const [chatState, setChatState] = React.useState({ state: "BUSINESS" });

  // Luego crearé un state que guarde la conversación actual. Dentro de cada lista habrá una serie de diccionarios, donde cada diccionario corresponde a una serie de mensajes seguidos y el display debe ser uno diccionario de chatbot y otro de human.
  const [chatMessages, setChatMessages] = React.useState({
    chatbot: [],
    human: [],
  });

  // Aquí tendré un api call que pida los mensajes de esta conversación al database. Tiene que tener un for loop en el que usamos la lista anterior para hacerle append a los mensajes.

  // Luego crearé la conexión con el api junto con axios
}
