import { fireEvent, render, screen } from '@testing-library/react'
import App from '../App'

test('renders upload component', () => {
  render(<App />)
  const uploadElement = screen.getByText(/Upload/i)
  expect(uploadElement).toBeInTheDocument()
  fireEvent.click(uploadElement)
  const uploadElement2 = screen.getByText(/Submit/i)
  expect(uploadElement2).toBeInTheDocument()
})

test('renders health status component', () => {
  render(<App />)
  const statusElement = screen.getByText(/Status/i)
  expect(statusElement).toBeInTheDocument()
})

test('renders search bar component', () => {
  render(<App />)
  const searchInput = screen.getByPlaceholderText(/Search for keywords to find related transcriptions/i)
  expect(searchInput).toBeInTheDocument()
})