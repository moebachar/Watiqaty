import React, { useState } from "react";
import { ChatEngine } from "react-chat-engine";
import { useLocation } from "react-router-dom";
import axios from "axios";
import {
  FileDoneOutlined,
  SaveOutlined,
  DeleteOutlined,
  RollbackOutlined,
  LockOutlined,
} from "@ant-design/icons";
import { Button, Menu } from "antd";

const CHATBOT_USERNAME = "chatbot";
const CHATBOT_SECRET = "123";

const addDocSection = (items, chat) => {
  let k = items[2].children.length + 1;
  const id = chat.id;
  const docSection = {
    id: id,
    key: "g" + k,
    label: chat.title,
    type: "group",
    children: [],
  };

  let it = [...items];
  it[2].children.push(docSection);
  return it;
};

const addDocument = (items, chatId, doc) => {
  let i;
  for (i = 0; i < items[2].children.length; i++) {
    if (items[2].children[i].id == chatId) {
      break;
    }
  }

  const key = items[2].children[i].children.length + 1;
  const docItem = {
    key: key,
    label: doc.title,
    disabeled: true,
    icon: <LockOutlined />,
  };

  let it = [...items];

  it[2].children[i].children.push(docItem);
  return it;
};

const ChatsPage = (props) => {
  const [chatId, setChatId] = useState(0);
  const [items, setItems] = useState([
    {
      key: "grp",
      label: "Contole",
      type: "group",
      children: [
        {
          key: "1",
          label: "Save Chat",
          icon: <SaveOutlined />,
        },
        {
          key: "2",
          label: "Delete Chat",
          icon: <DeleteOutlined />,
        },
        {
          key: "3",
          label: "Home",
          icon: <RollbackOutlined />,
        },
      ],
    },
    {
      type: "divider",
    },
    {
      key: "sub1",
      label: "Your Documents",
      icon: <FileDoneOutlined />,
      children: [
        {
          key: "g1",
          label: "Item 1",
          type: "group",
          children: [
            {
              id: 32,
              key: "4",
              label: "Demande Passport",
              disabeled: true,
              icon: <LockOutlined />,
            },
            {
              id: 33,
              key: "5",
              label: "Permit de conduite",
              disabeled: true,
              icon: <LockOutlined />,
            },
          ],
        },
      ],
    },
    {
      type: "divider",
    },
  ]);
  const location = useLocation();
  const user = location.state?.user;

  const handleSendMessage = (chatId, message) => {
    const data = { chat_id: chatId, message: message };
    setChatId(chatId);
    if (message.sender.username !== CHATBOT_USERNAME) {
      axios
        .post("http://localhost:3001/answer", data)
        .then((r) => console.log("success", r))
        .catch((e) => console.log("error", e));
    }
  };

  const handlenewChat = (chat) => {
    setChatId(chat.id);
    setItems(addDocSection(items, chat));
    axios
      .post(
        `https://api.chatengine.io/chats/${chat.id}/people/`,
        { username: CHATBOT_USERNAME },
        {
          headers: {
            "Project-ID": process.env.REACT_APP_CHAT_ENGINE_PROJECT_ID,
            "User-Name": user.username,
            "User-Secret": user.secret,
          },
        }
      )
      .then((r) => console.log("success", r))
      .catch((e) => console.log("error", e));
  };

  console.log("items", items);

  return (
    <div style={{ height: "100vh", width: "100vw", fontFamily: "Rubik" }}>
      <ChatEngine
        projectID={process.env.REACT_APP_CHAT_ENGINE_PROJECT_ID}
        userName={user.username} // adam
        userSecret={user.secret} // pass1234
        height="100vh"
        onNewMessage={handleSendMessage}
        onNewChat={handlenewChat}
        renderChatSettings={(chatAppState) => {
          console.log("chatAppState", chatId);
          return (
            <div>
              <Menu
                style={{
                  width: "100%",
                }}
                defaultSelectedKeys={["1"]}
                defaultOpenKeys={["sub1"]}
                mode="inline"
                items={items}
              />

              <Button
                onClick={() =>
                  setItems(addDocument(items, chatId, { title: "Attitation" }))
                }
              >
                Add Doc
              </Button>
            </div>
          );
        }}
      />
    </div>
  );
};

export default ChatsPage;
