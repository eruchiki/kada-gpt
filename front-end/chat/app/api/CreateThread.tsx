import axios from "axios";

const CreateThread = (userid: string, ThreadInfo: any, event: any) => {
  event.preventDefault()
  const url = `${process.env.API_URL}/chat/${userid}/thread`;
  const threadlist = axios.post(url,ThreadInfo);
};

export default CreateThread;
