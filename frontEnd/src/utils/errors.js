export default function handleErrors(response){
    if(!response.ok){
        console.log(response);
        throw Error(response.status);
    }else{
        return response;
    }
}