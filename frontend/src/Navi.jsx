import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';

export const Navi = () => {
  return (
    <Navbar bg="dark" variant="dark" expand="lg" className="justify-content-center">
      <Container>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/browse">일대일 과목 비교</Nav.Link>
            <Nav.Link href="/getclass">분반별 인원 조회</Nav.Link>
            <Nav.Link href="/getpeople">가입 인원 조회</Nav.Link>
            <Nav.Link href="/register">내 시간표 등록</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};
