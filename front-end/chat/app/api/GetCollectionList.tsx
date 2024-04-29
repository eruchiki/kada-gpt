import axios from "axios";

const GetCollectionList = async () => {
  const url = `${process.env.NEXT_PUBLIC_API_URL}/chat/collections`;
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

export default GetCollectionList;
