## Protocol Definition

The protocol for communication between the client and server consists of two main parts:

1. **Header (2 bytes)**: 
   - **Communication Code (1 byte)**: A single digit number specifying the type of request.
     - `1`: User Login
     - `2`: Retrieve Server Inventory
     - `4`: Make Purchase
     - `5`: User Logout
   - **Status Code (1 byte)**: An alphabet character denoting the status of the communication.
     - `S`: Success
     - `F`: Failure
     - `Z`: Item not found
     - `Y`: Item out of stock

2. **Body**: The actual data being sent, complex objects serialized using `pickle`.

### Example Messages

- **User Login Request**: 
  - Header: `1X`
  - Body: Serialized dictionary containing user credentials

- **Retrieve Server Inventory Request**:
  - Header: `2X`
  - Body: Empty

- **Make Purchase Request**:
  - Header: `4X`
  - Body: Serialized dictionary containing item UPC and quantity

- **User Logout Request**:
  - Header: `5X`
  - Body: Empty

### Serialization

All data in the body is serialized using `pickle` for complex objects and use of byte string for simple objects, before sending and deserialized upon receiving.