import axios from "axios";

const GetCollectionList = (userid: string) => {
  const url = `${process.env.API_URL}/chat/collection`;
  const collectionlist = axios.get(url);
  return collectionlist;
};

export default GetCollectionList;
