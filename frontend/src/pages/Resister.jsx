import { useState, useEffect } from "react"
import emailjs from '@emailjs/browser';
import { useNavigate } from "react-router-dom"
import axios from "axios"
export function Resister() {
    const client = axios.create()
    const navigate = useNavigate()
    const [userInfo, setUserInfo] = useState({
      'id' : '',
      'pw' : ''
    })
  // useEffect(()=>{
  //   alert("현재 인트라넷이 일시적으로 시간표 조정 기간에 있어 시간표 신규 등록이 불가합니다. 시간표 신규 등록은 PC버전 인트라넷에서 시간표가 조회되는 때를 시점으로 다시 가능합니다. 감사합니다.")
  // })
    const [msg, setMsg] = useState('')
    const [btnTxt, setBtnTxt] = useState('내 시간표 등록하기')
    const onClick = () => {
        setBtnTxt('로딩중...')
        client.post('https://api.hasclassmatching.com/api/resister', userInfo)
        .then(res=>{
          setBtnTxt('내 시간표 등록하기')
          if (res.data === 'success') {
            navigate('/browse')
          } else {
            setMsg(res.data)
          }
        })
        .catch(err=>{
          setMsg("예기치 못한 에러 발생")
          setBtnTxt('내 시간표 등록하기')
          emailjs.send('service_879kgqu', 'template_y2r986d', {});
        })
      }
    const onChange = (e) => {
        setUserInfo({
          ...userInfo,
          [e.target.name] : e.target.value
        })
      }
    return(
        <div id="contain">
            <h3>내 시간표 등록하기</h3>
            <input placeholder="인트라넷 아이디" id="in" onChange={onChange} name="id"/>
            <input placeholder="인트라넷 비밀번호" id="in" onChange={onChange} name="pw" type="password"/>
            <button variant="primary" type="submit" onClick={onClick} id='btn'>
              {btnTxt}
            </button>
            <br/>
            <label id='err'>{msg}</label>
        </div>
    )
}