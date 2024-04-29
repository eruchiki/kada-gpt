import axios from "axios";

const CreateThread = async (userid: string, ThreadInfo: any, event: any) => {
  event.preventDefault()
  const url = `${process.env.NEXT_PUBLIC_API_URL}/chat/users/${userid}/thread`;
  return await axios.post(url,ThreadInfo).then((response) => {
      return response.data;
    })
    .catch((error) => {
      // 失敗時の処理etc
      return error;
    });
};

export default CreateThread;
