import axios from "axios";

const GetThreadList = async (userid: number) => {
  const url = `${process.env.NEXT_PUBLIC_API_URL}/chat/users/${userid}/thread`;
  return await axios
    .get(url)
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      // 失敗時の処理etc
      return error;
    });
};

export default GetThreadList;
