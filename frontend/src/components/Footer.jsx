import React from 'react';
import AssemblyLogo from '../img/Assembly_Square_Logo.png';

export function Footer() {
  return (
    <footer style={styles.footer}>
      <p>© 2024 Seyong Ahn in HAS ASSEMBLY<img src={AssemblyLogo} alt='Assembly Logo' style={{width: '30px'}}/></p>
    </footer>
  );
};

const styles = {
  footer: {
    backgroundColor: 'white',
    textAlign: 'center',
    padding: '20px',
    position: 'fixed',
    left: '0',
    bottom: '0',
    width: '100%',
    height: '60px',
    'font-size': '12px'
  },
};
