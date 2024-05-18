import React, { useState } from "react";
import { Button, Form, Input, Typography, message } from "antd";
import { useNavigate } from "react-router-dom";
import "./login.css";
import axios from "axios";

function Login(props) {
  const [messageApi, contextHolder] = message.useMessage();
  const navigate = useNavigate();
  const success = () => {
    messageApi.success("Message Sent Successfully!");
  };

  const error = () => {
    messageApi.error("Failed to send message!");
  };

  const onFinish = (values) => {
    console.log("Success:", values);
    success();
    const userData = { username: values.username, secret: values.password };
    axios
      .post("http://localhost:3001/login", userData)
      .then((r) => navigate("/chat", { state: { user: userData } }))
      .catch((e) => console.log(JSON.stringify(e.response.data)));
  };
  const onFinishFailed = (errorInfo) => {
    error();
  };

  return (
    <div className="login">
      {contextHolder}
      <div className="login-form">
        <Typography.Title level={3}>
          Back to your digital documents
        </Typography.Title>
        <Typography.Paragraph>
          Choose one of the option to go
        </Typography.Paragraph>
        <Form
          name="basic"
          labelCol={{
            span: 8,
          }}
          wrapperCol={{
            span: 16,
          }}
          style={{
            maxWidth: 600,
          }}
          initialValues={{
            remember: true,
          }}
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
          autoComplete="off"
        >
          <Form.Item
            label="Username"
            name="username"
            rules={[
              {
                required: true,
                message: "Please input your Username!",
              },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Password"
            name="password"
            rules={[
              {
                required: true,
                message: "Please input your password!",
              },
            ]}
          >
            <Input.Password />
          </Form.Item>

          <Form.Item
            wrapperCol={{
              offset: 8,
              span: 16,
            }}
          >
            <Button type="primary" htmlType="submit">
              Log In
            </Button>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
}

export default Login;
