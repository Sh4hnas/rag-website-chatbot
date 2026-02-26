# Implementation Plan

- [x] 1. Set up custom CSS styling system





  - Inject custom CSS using st.markdown() with unsafe_allow_html=True at the top of app.py
  - Define CSS variables for color scheme (primary, secondary, user/bot message colors, backgrounds)
  - Create base styles for message bubbles with rounded corners, shadows, and proper alignment
  - Style buttons with hover effects and disabled states
  - Style input fields with focus states and borders
  - Create card styles for metadata and summary display
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

- [x] 2. Implement chat message data model and session state




  - Create ChatMessage dataclass with role, content, timestamp, and optional sources fields
  - Create WebsiteMetadata dataclass with url, processed_at, chunk_count, status, title, and error_message
  - Initialize enhanced session state structure including messages list, website_metadata, and ui_state
  - Add helper function to convert ChatMessage to dictionary format
  - _Requirements: 1.1, 1.2, 1.3, 7.5_

- [x] 3. Build chat message display component





  - Create display_message() function that generates HTML for individual messages
  - Implement different styling for user vs assistant messages (right/left alignment)
  - Add timestamp display to each message
  - Include markdown rendering support for formatted text
  - Add avatar/icon indicators for user and bot
  - _Requirements: 1.1, 1.2, 1.5, 4.4_

- [x] 4. Implement chat history management system





  - Create add_message() function to append messages to session state
  - Create render_chat_history() function to display all messages in scrollable container
  - Implement auto-scroll to newest message when conversation history exceeds viewport
  - Add typing indicator animation display during bot response generation
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.6, 7.5_
-

- [x] 5. Reorganize layout with sidebar and main content area




  - Configure page with st.set_page_config() for wide layout and expanded sidebar
  - Move URL input and Process Website button to sidebar
  - Create sidebar section for website metadata display (title, chunk count, status)
  - Move Generate Summary button to sidebar
  - Keep main content area for chat interface
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [x] 6. Enhance website processing with better feedback




  - Add loading state to Process Website button (disable during processing)
  - Display processing status with spinner and descriptive text
  - Show success notification when processing completes
  - Update website metadata in session state with processed_at timestamp
  - Display website metadata card in sidebar after successful processing
  - Implement error handling with user-friendly messages for URL processing failures
  - _Requirements: 3.3, 3.4, 5.4, 6.1, 6.2, 6.3_
-

- [x] 7. Implement enhanced question input and submission



  - Replace basic text input with form-based input to support Enter key submission
  - Add validation to prevent empty question submission
  - Disable question input when no website has been processed with helpful message
  - Add loading state to submit button during answer generation
  - _Requirements: 3.2, 3.5, 3.6, 6.4_


- [x] 8. Integrate answer generation with chat history







  - Modify answer generation to add user question to chat history immediately
  - Display typing indicator while generating answer
  - Add bot response to chat history after generation
  - Store source chunk indices with assistant messages
  - Render updated chat history after each interaction
  - _Requirements: 1.1, 1.2, 1.3, 1.6_
-

- [x] 9. Enhance source chunks display




  - Display source chunks in collapsible expanders below the answer in chat
  - Number each source chunk for easy reference
  - Add relevance indicators (distance scores) to source chunks
  - Format source chunks with proper styling
  - _Requirements: 4.2, 4.3_

- [x] 10. Implement clear chat functionality





  - Add "Clear Chat" button to sidebar
  - Implement confirmation dialog before clearing chat history
  - Clear messages from session state while maintaining website data
  - Show success notification after clearing
  - _Requirements: 7.1, 7.2, 7.3_

- [x] 11. Improve summary generation display




  - Format summary output in a visually distinct card
  - Add summary to chat history as a bot message
  - Display summary with proper bullet points and markdown rendering
  - Show chunk count and processing metadata
  - _Requirements: 4.1, 4.4_

- [x] 12. Add comprehensive error handling and validation





  - Implement URL format validation before processing
  - Add try-catch blocks for network errors with user-friendly messages
  - Handle content extraction errors gracefully
  - Implement error handling for LLM generation failures
  - Display validation messages for invalid user actions
  - Add helpful messages when chatbot cannot answer questions
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 13. Implement accessibility improvements





  - Ensure all interactive elements have proper focus indicators
  - Use readable font sizes (16px base) and sufficient contrast ratios
  - Add ARIA labels to status messages and interactive elements
  - Test keyboard navigation for all functionality
  - Ensure visual feedback for all user actions
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_
-

- [x] 14. Add status indicators and notifications system



  - Implement processing status display (processing, ready, error) in sidebar
  - Use st.success(), st.error(), st.warning() for appropriate feedback
  - Add toast notifications for quick feedback on actions
  - Show progress indicators with descriptive text for long operations
  - _Requirements: 4.5, 6.2, 6.3_

- [x] 15. Optimize performance and session management





  - Limit chat history display to last 50 messages with load more option
  - Ensure CSS is injected once at startup, not on every rerun
  - Verify st.cache_resource is used for model loading
  - Minimize unnecessary session state updates
   - Test session persistence across interactions
  - _Requirements: 1.3, 7.5_
