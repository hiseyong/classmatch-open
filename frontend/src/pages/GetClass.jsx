import Accordion from 'react-bootstrap/Accordion';
import axios from "axios"
import { useState, useEffect } from "react"
import emailjs from '@emailjs/browser';
export function GetClass() {
    const client = axios.create()
    const [userInfo, setUserInfo] = useState({
      'id' : ''
    })
    const [rec, setRec] = useState([])
    const [classes, setClasses] = useState(null)
    const [msg, setMsg] = useState('')
    const [btnTxt, setBtnTxt] = useState('분반 인원 조회하기')
  
    useEffect(()=>{
      const storedValue = localStorage.getItem('id');
      console.log(storedValue)
      if (storedValue && storedValue.length === 5) {
        setUserInfo({
          ...userInfo,
          'id': storedValue
        })
      }
    },[])
  
    const onClick = () => {
      setBtnTxt('로딩중...')
      client.post('https://api.hasclassmatching.com/api/getclass', userInfo)
      .then(res=>{
        setBtnTxt('분반 인원 조회하기')
        if(typeof(res.data) === 'string') {
          setRec([])
          setMsg(res.data)
        } else {
          localStorage.setItem('id', userInfo.id);
          setMsg('')
          setRec(res.data)
        }
      })
      .catch(err=>{
        setMsg('예기치 못한 에러 발생')
        setBtnTxt('겹치는 과목 조회하기')
        emailjs.send('service_879kgqu', 'template_y2r986d', {});
      })
    }

    useEffect(()=>{
        let temp = []
        for(let i in rec) {
            temp.push(
                <Accordion defaultActiveKey="0">
                    <Accordion.Item eventKey="1">
                        <Accordion.Header>{i+' '+rec[i][0]+'분반'}</Accordion.Header>
                        <Accordion.Body>
                            {rec[i][1].map((elem)=><h5>{elem}</h5>)}
                        </Accordion.Body>
                    </Accordion.Item>
                    <hr/>
                </Accordion>
            )
        }
        setClasses(temp)
    },[rec])
  
    
    const onChange = (e) => {
      setUserInfo({
        ...userInfo,
        [e.target.name] : e.target.value
      })
    }
    return(
        <div id='contain'>
            <h3>분반 인원 조회하기</h3>
            <input placeholder='나의 고유학번' id='in' onChange={onChange} name='id' value={userInfo.id}/>
            <button variant="primary" type="submit" onClick={onClick} id='btn'>
                {btnTxt}
            </button>
            <br/>
            <label id='err'>{msg}</label>
            <br/>
            <div id="classescontainer">
                {classes}
            </div>
        </div>
    )
}