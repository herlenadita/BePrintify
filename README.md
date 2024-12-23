# `BePrintify`
<a href="https://rohan-hari.github.io/Postman-Clone-React/">Live Demo</a> 

Welcome to your new `BePrintify` project and to the Internet Computer development community. By default, creating a new project adds this README and some template files to your project directory. You can edit these template files to customize your project and to include your own code to speed up the development cycle.

To get started, you might want to explore the project directory structure and the default configuration file. Working with this project in your development environment will not affect any production deployment or identity tokens.

To learn more before you start working with `BePrintify`, see the following documentation available online:

- [Quick Start](https://internetcomputer.org/docs/current/developer-docs/setup/deploy-locally)
- [SDK Developer Tools](https://internetcomputer.org/docs/current/developer-docs/setup/install)
- [Motoko Programming Language Guide](https://internetcomputer.org/docs/current/motoko/main/motoko)
- [Motoko Language Quick Reference](https://internetcomputer.org/docs/current/motoko/main/language-manual)

If you want to start working on your project right away, you might want to try the following commands:

```bash
cd BePrintify/
dfx help
dfx canister --help
```

## Running the backend project locally

If you want to test your project locally, you can use the following commands:

```bash
# Starts the replica, running in the background
dfx start --background

# Deploys your canisters to the replica and generates your candid interface
dfx deploy
```

Once the job completes, your application will be available at `http://localhost:4943?canisterId={asset_canister_id}`.

```bash
python3 PrintService.py
```

Which will start a server at `http://localhost:5000`

### Running the frontend project locally

- A front-end of printify using React JS. This website can be used for accessing resources on web via HTTP. It helps users hit in Printify API.
- https://github.com/herlenadita/FePrintify

## License

MIT
