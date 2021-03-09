describe('Visit WhiteJaguars Demo site', () => {
  it('Sanity check', () => {
    cy.visit('http://192.168.1.60:8000')
  })
})