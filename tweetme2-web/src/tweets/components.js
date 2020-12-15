import React ,{useEffect, useState } from 'react'
import {apiTweetAction, apiTweetCreate,apiTweetList} from './lookup'

export function TweetsComponents(props){
  const textAreaRef = React.createRef()
  const[newTweets ,setNewTweets]=useState([])
  //Making it a Server side call backend api response handler
  const handleBackendUpdate=(response,status)=>{
    let tempNewTweets=[...newTweets]
    if(status===201){
      tempNewTweets.unshift(response)
      setNewTweets(tempNewTweets)
    }else{
      console.log(response)
      alert("an error occured please try again")
   }
  }
  const handleSubmit=(event)=>{
     event.preventDefault()
     const newVal=textAreaRef.current.value
     //backend endapi request
     apiTweetCreate(newVal,handleBackendUpdate) 
     textAreaRef.current.value=''

  }
  return <div className={props.className}>
           <div className='col-12 mb-3'>
             <form onSubmit={handleSubmit}>
                <textarea ref={textAreaRef} required = {true} classname='form-control'>
      
                </textarea>
                   <button type='submit' className='btn btn-primary my-3'>Tweet</button>
              </form>
            </div>
       <  TweetList/>
         </div>
}


  export function TweetList(props){
    const [tweetsInit,setTweetsInit]=useState([])
    const [tweets,setTweets]=useState([])
    const [tweetsDidSet,setTweetsDidSet]=useState(false)
    useEffect(()=>{ 
      const final=[...props.newTweets].concat(tweetsInit)
      if(final.length!==tweets.length){
       setTweets(final)
     }
    }, [props.newTweets,tweets,tweetsInit])

    useEffect(()=>{
      if(tweetsDidSet===false){
      const handleTweetListLookup=(response,status)=>{
        console.log(response,status)
        if(status===200){
        setTweetsInit(response)
        setTweetsDidSet(true) 
        }  
      }
      apiTweetList(handleTweetListLookup)
    }
    },[tweetsInit,tweetsDidSet,setTweetsDidSet])
    return tweetsInit.map((item,index)=>{
      return <Tweet tweet={item} className='my-5 py-5 border bg-green text-dark' key={`${index}-{item.id}`}/>
    })
  }

export function ActionBtn(props){
    const {tweet,action}=props
    const [likes,setLikes ]=useState(tweet.likes ? tweet.likes:0)
    // const [userLike,setUserLike]=useState(tweet.userLike===true ? true :false)
    const {className}=props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay=action.display ? action.display:'Action'
    const handleActionBackendEvent=(response,status)=>{
      console.log(response,status)
      if(status===200){
        setLikes(response.likes)
      }
    }
    const handleClick=(event)=>{
      event.preventDefault()
      apiTweetAction(tweet.id,action.type,handleActionBackendEvent)
      
    }
    const display=action.type==='like'? `${likes} ${actionDisplay}`:action.display
    return <button className={className} onClick={handleClick}> {display}</button>
  }

  export function ParentTweet(props){
   const{tweet}=props

    return tweet.parent ? <div className='row'>
            <div className='col-11 mx-auto p-3 border rounded'>
           <p className='mb-0 text-muted small'>Retweet</p>
           <Tweet className={' '} tweet={tweet.parent}/>
          </div>
        </div>:null
  }
  
export function Tweet(props){
    const  {tweet}=props
    const {className}=props.className ? props.className : 'col-10 mx-auto '
    return <div className={className}>
      <div>
        <p>{tweet.id} - {tweet.content}</p>
        <ParentTweet tweet = {tweet}/>
      </div>
      <div className='btn btn-group'>
        <ActionBtn tweet={tweet} action={{type:"like",display:'Likes'}}/>
        <ActionBtn tweet={tweet} action={{type:"unlike",display:'unlike'}}/>
        <ActionBtn tweet={tweet} action={{type:"retweet",display:'Retweet'}}/>
        
      </div>
    </div>
  }
  