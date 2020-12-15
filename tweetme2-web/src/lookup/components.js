export function backendlookup(method,endpoint,callback,data){
  let jsonData;
  if(data){
    jsonData=JSON.stringify(data)
  }
    const xhr=new XMLHttpRequest() //someclass instance //post
    const url=`http://localhost:8000/api${endpoint}`
    xhr.responseType="json"
    xhr.open(method,url)
    // eslint-disable-next-line no-undef
    const csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader("content=Type","application/json")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH","XMLHttpRequest")
    xhr.setRequestHeader("X_REQUESTED_WITH","XMLHttpRequest")
    xhr.setRequestHeader("x-CSRFTOKEN",csrftoken)
    xhr.onload=function(){
      callback(xhr.response,xhr.status)
    }
    xhr.onerror=function(e){ 
    console.log(e)
    callback({"message":"the request was an error"},400) 
    }
  xhr.send(jsonData)    
  }




  