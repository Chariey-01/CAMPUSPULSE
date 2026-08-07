import { ChevronLeft, ChevronRight } from 'lucide-react'

export default function Pagination({ page, totalPages, onPageChange }) {
  if (totalPages <= 1) {
    return null
  }

  return (
    <div className="pagination">
      <button className="btn-ghost" disabled={page <= 1} onClick={() => onPageChange(page - 1)}>
        <ChevronLeft size={15} /> Previous
      </button>
      <span>Page {page} of {totalPages}</span>
      <button className="btn-ghost" disabled={page >= totalPages} onClick={() => onPageChange(page + 1)}>
        Next <ChevronRight size={15} />
      </button>
    </div>
  )
}
