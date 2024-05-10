import GetCollectionList from "./GetCollectionList"
import GetUser from "./GetUser";


const PopUpFunction = async (userid:number) => {
  const CollectionList = await GetCollectionList();
  const UserInfo = await GetUser(userid);
  const NewCollectionList = CollectionList.map((collection) => ({
    id: collection.id,
    name: collection.name,
  }));
  return {GroupId:UserInfo.group_id, CollectionList:NewCollectionList}
};

export default PopUpFunction;
