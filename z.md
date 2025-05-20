```mermaid
ClassDiagram
    class User {
        +id: Integer
        +username: String
        +email: String
        +password: String
        +first_name: String
        +last_name: String
        +address: String
        +phone_number: String
    }

    class Agent {
        +agency_name: String
        +license_number: String
    }

    class Landlord {
        +properties: List<Property>
    }

    class Tenant {
        +rented_properties: List<Property>
    }

    class Property {
        +id: Integer
        +address: String
        +price: Float
        +description: String
        +available_from: Date
        +type: String
        +landlord: Landlord
    }

    User <|-- Agent
    User <|-- Landlord
    User <|-- Tenant

    Landlord "1" --> "0..*" Property : owns >
    Tenant "0..*" --> "0..*" Property : rents >
10