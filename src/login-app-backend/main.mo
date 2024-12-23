import HashMap "mo:base/HashMap";
import Text "mo:base/Text";
import Hash "mo:base/Hash";
import Iter "mo:base/Iter";
import Array "mo:base/Array";
import Debug "mo:base/Debug";


actor Backend {
    type User = { username: Text; password: Text };
    type Template = { templatename: Text; content : Text };
    stable var users : [ User ] = [];
    stable var templates : [ Template ] = [];

    
    public func addUser(user:User) : async Text {
        // Check if the username already exists
        let userfind=await findUser(user);
        switch (userfind) {
          case (?_) { 
            return "Error: Username already exists.";
            };
          case null { 
            users := Array.append(users, [user]);
            return "User added successfully.";
            };
        };
        // Add the new user
        
    };

    

    // Function to authenticate a user
    public func login(user:User) : async Text {
        // Check if the user exists with the correct password
        switch (await findLoginUser(user)) {
          case (?_) { 
            return "Login successful!";
            };
          case null { 
            return "Invalid credentials!."; 
            };
        };
    };
    

    // Function to list all users (for testing purposes)
    public query func listUsers() : async [Text] {        
        return Array.map<User,Text>(users, func x = x.username);
    };

    public func addTemplate(template:Template) : async Text {
         templates := Array.append(templates, [template]);
         return "{\"message\":\"Template added successfully.\",\"template_name\":\""#template.templatename#"\"}";
        
    };

    public func getTemplate(templatename:Text) : async Text {
        var item:?Template=await findTemplate(templatename);
        switch (item) {
          case (?item) { 
            return item.content;
            };
          case null { 
            return ""; 
            };
        };
        
    };
    

    //internal/non api function


    public func findTemplate(templatename:Text): async ?Template {
        let actual : ?Template = Array.find<Template>(templates, func (x : Template) : Bool {
            x.templatename == templatename
          });
        return actual;
    };
    public func findUser(user: User): async ?User {
        let actual : ?User = Array.find<User>(users, func (x : User) : Bool {
            x.username == user.username
          });
        return actual;
    };

    public func findLoginUser(user: User): async ?User {
        let actual : ?User = Array.find<User>(users, func (x : User) : Bool {
            x.username == user.username and x.password== user.password
          });
        return actual;
    };

    func stringifyUser(user: User): Text {
        return "{" # "\"username\": \"" # user.username # "\", \"password\": \"" # user.password # "\"}";
    };

    func stringifyArray(users: [User]): Text {
        var usertext:[Text]=Array.map<User, Text>(users, stringifyUser);
        var result:Text ="[";
        for (i in Iter.range(0, Array.size(usertext) - 1)) {
          result #= stringifyUser(users[i]);
        };
        result #= "]";
        return result;
    };
};
