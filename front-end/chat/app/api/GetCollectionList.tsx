import axios from "axios";

const GetCollectionList = async (group_id:number) => {
  const url = `${process.env.NEXT_PUBLIC_API_URL}/chat/collections/${group_id}`;
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
