import axios from "axios";

const CreateThread = (userid: string, ThreadInfo: any, event: any) => {
  event.preventDefault()
  const url = `${process.env.HOST_URL}/chat/${userid}/thread`;
  const threadlist = axios.post(url,ThreadInfo);
};

export default CreateThread;
