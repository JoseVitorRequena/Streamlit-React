import React from 'react'

const Header = () => (
  <div style={{
    background: 'linear-gradient(135deg, #6e48aa 0%, #9d50bb 100%)',
    color: 'white',
    padding: '2rem',
    borderRadius: '0.5rem',
    marginBottom: '2rem',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
  }}>
    <h1 style={{ margin: 0, fontSize: '2.5rem' }}>Análise Educacional Avançada</h1>
    <p style={{ margin: '0.5rem 0 0', fontSize: '1.1rem' }}>
      Dashboard interativo para análise de desempenho estudantil
    </p>
    <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
      <span style={{ background: 'rgba(255,255,255,0.2)', padding: '0.3rem 0.8rem', borderRadius: '1rem', fontSize: '0.9rem' }}>
        📊 Visualização de Dados
      </span>
      <span style={{ background: 'rgba(255,255,255,0.2)', padding: '0.3rem 0.8rem', borderRadius: '1rem', fontSize: '0.9rem' }}>
        🎯 Insights Educacionais
      </span>
    </div>
  </div>
)

export default Header