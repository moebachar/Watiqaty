import React, { useEffect } from "react";
import logo from "../assets/svg/logo.svg";
import fig1 from "../assets/svg/fig1.svg";
import morocco from "../assets/svg/morocco.svg";
import um6p from "../assets/images/um6p.png";
import adria from "../assets/images/adria.png";
import college from "../assets/images/college-of-computing.png";
import Lottie from "react-lottie";
import animationData from "../assets/animations/animation2.json"; // Path to your JSON file
import { Button, Flex, Typography, Form, Input, message } from "antd";
import "./landingPage.css";
import { motion } from "framer-motion";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { SendOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

const settings = {
  dots: false,
  infinite: true,
  speed: 500,
  slidesToShow: 3,
  slidesToScroll: 1,
  autoplay: true,
  autoplaySpeed: 2000,
  cssEase: "linear",
};

const defaultOptions = {
  loop: false,
  autoplay: true,
  animationData: animationData,
  rendererSettings: {
    preserveAspectRatio: "xMidYMid slice",
  },
};

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { delay: 0.5, duration: 0.5 },
  },
  exit: {
    opacity: 0,
    transition: { ease: "easeInOut" },
  },
};

function LandingPage(props) {
  const [messageApi, contextHolder] = message.useMessage();
  const navigate = useNavigate();

  const success = () => {
    messageApi.success("Message Sent Successfully!");
  };

  const error = () => {
    messageApi.error("Failed to send message!");
  };

  const onFinish = (values) => {
    success();
  };
  const onFinishFailed = (errorInfo) => {
    error();
  };

  return (
    <div className="landing-page">
      {contextHolder}
      <header className="header">
        <div className="logo">
          <img src={logo} alt="logo" className="logo-image" />
        </div>
        <nav className="navbar">
          <Flex gap="small" wrap>
            <Button type="text" href="#home">
              Home
            </Button>
            <Button type="text" href="#services">
              Services
            </Button>
            <Button type="text" href="#partners">
              Partners
            </Button>
            <Button type="text" href="#contact">
              Contact Us
            </Button>
          </Flex>
        </nav>
        <Button className="login-button" onClick={() => navigate("/login")}>
          Login
        </Button>
      </header>
      <motion.section
        id="home"
        className="sec1"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7, duration: 0.5 }}
      >
        <div className="sec1-content">
          <div className="text">
            <Typography.Title level={1}>
              Simplifying Paperwork <br /> for Every Moroccan{" "}
              <img src={morocco} alt="morocco" className="morocco" />
            </Typography.Title>
            <Typography.Paragraph>
              Streamline your document processing with ease and efficiency.
            </Typography.Paragraph>
          </div>
          <div className="buttons">
            <Button type="primary">Get Started</Button>
            <Button type="text">Sign Up</Button>
          </div>
        </div>
        <Lottie
          options={defaultOptions}
          style={{
            width: "35%", // Set the width to 35% of the parent container
            margin: 0,
          }}
        />
      </motion.section>
      <motion.section
        id="services"
        className="sec2"
        initial={{ opacity: 0, x: 30 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 1, duration: 0.5 }}
      >
        <img className="sec2-image" src={fig1} alt="fig1" />
        <div className="sec2-content">
          <div className="text">
            <Typography.Title level={1}>
              Quick Access to <br /> Administrative Services
            </Typography.Title>
            <Typography.Paragraph>
              Obtain all required government documents without the hassle.
            </Typography.Paragraph>
          </div>
          <div className="buttons">
            <Button type="primary">Explore Services</Button>
            <Button type="text">Learn More</Button>
          </div>
        </div>
      </motion.section>
      <Typography.Title level={1} style={{ marginBottom: 50 }}>
        Our Partners
      </Typography.Title>
      <motion.section
        id="partners"
        className="sec3"
        initial={{ opacity: 0, x: 30 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 1, duration: 0.5 }}
      >
        <div className="carousel-container">
          <div className="carousel-slide">
            <img className="sec3-image" src={um6p} alt="UM6P" id="um6p" />
            <img
              className="sec3-image"
              src={college}
              alt="College of Computing"
            />
            <img
              className="sec3-image"
              src="https://thinkai.ma/img/FACE.svg"
              alt="FACE Academy"
            />
            <img
              className="sec3-image"
              src="https://thinkai.ma/img/logo.svg"
              alt="FACE Academy"
            />
            <img className="sec3-image" src={adria} alt="Adria" />
            <img
              className="sec3-image"
              src="https://thinkai.ma/img/1337.svg"
              alt="1337"
            />
            {/* Duplicate set of images for smooth looping */}
            <img className="sec3-image" src={um6p} alt="UM6P" id="um6p" />
            <img
              className="sec3-image"
              src={college}
              alt="College of Computing"
            />
            <img
              className="sec3-image"
              src="https://thinkai.ma/img/FACE.svg"
              alt="FACE Academy"
            />
            <img
              className="sec3-image"
              src="https://thinkai.ma/img/logo.svg"
              alt="FACE Academy"
            />
            <img className="sec3-image" src={adria} alt="Adria" />
            <img
              className="sec3-image"
              src="https://thinkai.ma/img/1337.svg"
              alt="1337"
            />
            <img className="sec3-image" src={um6p} alt="UM6P" id="um6p" />
            <img
              className="sec3-image"
              src={college}
              alt="College of Computing"
            />
            <img
              className="sec3-image"
              src="https://thinkai.ma/img/FACE.svg"
              alt="FACE Academy"
            />
            <img className="sec3-image" src={adria} alt="Adria" />
            <img
              className="sec3-image"
              src="https://thinkai.ma/img/1337.svg"
              alt="1337"
            />
            <img className="sec3-image" src={um6p} alt="UM6P" id="um6p" />
            <img
              className="sec3-image"
              src={college}
              alt="College of Computing"
            />
            <img
              className="sec3-image"
              src="https://thinkai.ma/img/FACE.svg"
              alt="FACE Academy"
            />
            <img
              className="sec3-image"
              src="https://thinkai.ma/img/logo.svg"
              alt="FACE Academy"
            />
            <img className="sec3-image" src={adria} alt="Adria" />
            <img
              className="sec3-image"
              src="https://thinkai.ma/img/1337.svg"
              alt="1337"
            />
            <img className="sec3-image" src={um6p} alt="UM6P" id="um6p" />
            <img
              className="sec3-image"
              src={college}
              alt="College of Computing"
            />
            <img
              className="sec3-image"
              src="https://thinkai.ma/img/FACE.svg"
              alt="FACE Academy"
            />
            <img
              className="sec3-image"
              src="https://thinkai.ma/img/logo.svg"
              alt="FACE Academy"
            />
            <img className="sec3-image" src={adria} alt="Adria" />
            <img
              className="sec3-image"
              src="https://thinkai.ma/img/1337.svg"
              alt="1337"
            />
          </div>
        </div>
      </motion.section>
      <Typography.Title level={1} style={{ marginBottom: 50, marginTop: 100 }}>
        Contact Us
      </Typography.Title>
      <motion.section
        id="contact"
        className="sec4"
        initial={{ opacity: 0, x: 30 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 1, duration: 0.5 }}
      >
        <div>
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 8,
            }}
            initialValues={{
              remember: true,
            }}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
            className="contact-form"
          >
            <Form.Item label="Full Name" name="fullname">
              <Input />
            </Form.Item>

            <Form.Item
              label="E-mail"
              name="email"
              rules={[
                {
                  required: true,
                  message: "Please input your E-mail!",
                },
              ]}
              placeholder="example@xyz.com"
            >
              <Input />
            </Form.Item>

            <Form.Item
              name="message"
              label="Message"
              rules={[
                {
                  required: true,
                  message: "Please input your Message!",
                },
              ]}
            >
              <Input.TextArea />
            </Form.Item>

            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button type="primary" htmlType="submit" icon={<SendOutlined />}>
                Submit
              </Button>
            </Form.Item>
          </Form>
        </div>
      </motion.section>
      <footer>
        <div>
          <img src={logo} alt="logo" width={200} />
          <Typography.Paragraph style={{ color: "#fff", marginTop: 30 }}>
            © 2024 ThinkAI. All Rights Reserved.
          </Typography.Paragraph>
        </div>
        <div>
          <nav className="navbar">
            <Flex direction="column" gap="small">
              <Button type="text" style={{ color: "#fff" }} href="#home">
                Home
              </Button>
              <Button type="text" style={{ color: "#fff" }} href="#services">
                Services
              </Button>
              <Button type="text" style={{ color: "#fff" }} href="#partners">
                Partners
              </Button>
              <Button type="text" style={{ color: "#fff" }} href="#contact">
                Contact Us
              </Button>
            </Flex>
          </nav>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage;
