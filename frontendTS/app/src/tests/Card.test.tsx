import { fireEvent, render, screen } from '@testing-library/react'
import Card from '../components/Card'

test('renders Card component', () => {
  render(<Card
    header="header"
    subtitle="subtitleT"
    upload_path="upload_path"
    text="text"
    searchTerm="searchTerm"
    setReload={()=>{}}
  />)
  const cardElement = screen.getByText(/header/i)
  expect(cardElement).toBeInTheDocument()
  const cardElement2 = screen.getByText(/subtitle/i)
  expect(cardElement2).toBeInTheDocument()
})

test('view card details', () => {
  render(<Card
    header="header"
    subtitle="subtitle"
    upload_path="upload_path"
    text="text"
    searchTerm="text"
    setReload={()=>{}}
  />)
  fireEvent.click(screen.getByText(/View Details/i))
  const cardElement3 = screen.getByText(/text/i)
  expect(cardElement3).toBeInTheDocument()
  const cardElement4 = screen.getByText(/Close/i)
  expect(cardElement4).toBeInTheDocument()
})