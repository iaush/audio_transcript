import { fireEvent, render, screen } from '@testing-library/react'
import Card from '../components/Card'

test('renders Card component', () => {
  const testSubtitle = "2025-01-17T12:00:00Z";
  render(<Card
    header="header"
    subtitle={testSubtitle}
    upload_path="upload_path"
    text="text"
    searchTerm="searchTerm"
    setReload={()=>{}}
  />)
  const cardElement = screen.getByText(/header/i)
  expect(cardElement).toBeInTheDocument()
  const formattedDate = new Date(testSubtitle).toLocaleString();
  const cardSubtitle = screen.getByText(new RegExp(`Upload Date: ${formattedDate}`));
  expect(cardSubtitle).toBeInTheDocument();
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