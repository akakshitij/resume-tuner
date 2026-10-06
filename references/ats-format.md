# Format rules that get a resume parsed

Most large employers screen with an ATS (applicant tracking system) before a person sees the
resume. A pretty layout that the parser can't read loses before the content counts.

| Rule | Why |
|---|---|
| **Single column** | Two-column layouts get read across the columns, scrambling lines |
| **No tables, text boxes, icons, images or graphics** | Parsers skip or garble them; skills in an icon grid vanish |
| **Standard headings**: Experience, Education, Skills, Projects | The parser looks for these words to split sections |
| **Reverse chronological** | Most recent first, which is what both the parser and the recruiter expect |
| **PDF**, unless the application asks for .docx | Keeps the layout; text must be selectable, never a scanned image |
| **One page** under ~10 years of experience | Recruiters skim; page two rarely gets read |
| **Job title and dates on one line per role** | Parsers pair them to calculate experience |
| **Keywords in the job's exact wording** where true | Matching is often literal: "UX research" won't match "user research" |
| **Contact details in the body**, not a header or footer | Some parsers ignore headers and footers |
| **Clean metadata** | Title and author set, no generator names in `/Producer` or `/Creator` |

Quick test: copy all the text out of the PDF and paste it into a plain text editor. If the order
is wrong or words are missing, the ATS sees the same mess.
