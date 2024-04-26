import axios from "axios";

const GetCollectionList = (userid: string) => {
  const url = `${process.env.HOST_URL}/chat/collection`;
  const collectionlist = axios.get(url);
  return collectionlist;
};

export default GetCollectionList;
