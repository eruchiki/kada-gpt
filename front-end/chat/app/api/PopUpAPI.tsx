import GetCollectionList from "./GetCollectionList"
import GetUser from "./GetUser";


const PopUpFunction = async (userid: number) => {
  const UserInfo = await GetUser(userid);
  const CollectionList = await GetCollectionList(UserInfo.group_id);
  const NewCollectionList = CollectionList.map((collection) => ({
    id: collection.id,
    name: collection.name,
  }));
  return {GroupId:UserInfo.group_id, CollectionList:NewCollectionList}
};

export default PopUpFunction;
