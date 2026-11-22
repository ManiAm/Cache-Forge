# Artifactory

During the software build process, developers produce various **artifacts** — libraries, packages, binaries, and container images that are needed for application deployment and runtime. An **artifact repository manager** is a tool that provides a centralized platform for storing, versioning, and distributing these artifacts.

[JFrog Artifactory](https://jfrog.com/artifactory/) is the repository manager used by Cache-Forge. Before diving into Artifactory specifically, here is why artifact management matters:

- **CI/CD Integration** — Code is built and tested automatically in CI/CD pipelines. A repository manager stores the build outputs (`.jar`, `.deb`, `.whl`, Docker images, etc.) so they can be promoted across environments (dev → test → prod) without rebuilding.

- **Version Control for Binaries** — Multiple versions of the same artifact are retained, allowing teams to roll back, debug, or recreate previous environments.

- **Dependency Caching** — External libraries are cached locally, speeding up builds and protecting against outages when public registries are slow or unavailable.

## Comparison of Artifact Repository Managers

Over the years, many artifact repository managers have been developed. They vary in capabilities, format support, and deployment models.

| Tool | Year | Description |
|---|---|---|
| **JFrog Artifactory** | 2006 | Universal artifact manager supporting 30+ formats with deep CI/CD integrations. Used by Cache-Forge. |
| **Apache Archiva** | 2007 | One of the earliest repository managers, focused on Maven artifacts. Lightweight and open-source. |
| **Sonatype Nexus** | 2008 | Widely used manager supporting Maven, npm, Docker, and more. Available in OSS and Pro editions. |
| **Cloudsmith** | 2016 | Fully managed, cloud-native repository supporting Docker, npm, Python, RubyGems, and others. |
| **Azure Artifacts** | 2018 | Part of Azure DevOps. Supports Maven, npm, NuGet, and Python with tight Azure CI/CD integration. |
| **GitLab Package Registry** | 2018 | GitLab's built-in package manager supporting Docker, Maven, npm, Conan, and others. |
| **GitHub Packages** | 2019 | GitHub's artifact storage for Docker, npm, RubyGems, NuGet, and more. Integrated with GitHub Actions. |
| **AWS CodeArtifact** | 2020 | Managed artifact service by AWS. Supports Maven, npm, PyPI, and NuGet with IAM integration. |
| **Google Artifact Registry** | 2020 | Unified artifact storage in Google Cloud for Docker, Maven, npm, and more. Replaces Google Container Registry. |

## JFrog Artifactory

JFrog Artifactory is one of the most widely adopted artifact repository managers in the industry. It is available in multiple editions — from a free open-source version to commercial editions for large-scale enterprises. Artifactory supports over 30 package types, making it a single platform for managing artifacts regardless of technology stack.

### Supported Package Types

| Category | Formats |
|---|---|
| Build Tools | Maven, Gradle, Ivy, SBT |
| JavaScript | npm, Bower |
| Python | PyPI, Conda |
| .NET | NuGet |
| Ruby | RubyGems |
| Apple (iOS/macOS) | CocoaPods |
| C/C++ | Conan |
| Go | Go |
| Rust | Cargo |
| R | CRAN |
| PHP | Composer |
| Dart | Pub |
| Swift | Swift |
| Linux Packages | Debian, RPM, opkg |
| Config Management | Ansible, Chef, Puppet |
| Containers & Orchestration | Docker, OCI, Terraform, Helm |
| VM Provisioning | Vagrant |
| Git Large Files | GitLFS |

### Repository Types

A **repository** in Artifactory is a structured storage location for software artifacts. Repositories enable versioned storage, access control, and artifact retrieval for both developers and CI/CD pipelines. Artifactory supports three repository types:

| Type | Purpose |
|---|---|
| **Local** | Stores artifacts deployed directly by internal teams or build systems. Used for proprietary packages and internal build outputs. |
| **Remote** | Acts as a caching proxy for external registries (e.g., PyPI, Maven Central, Docker Hub). Fetches from upstream on the first request, then serves from cache. |
| **Virtual** | Aggregates multiple local and remote repositories into a single unified endpoint. Simplifies client configuration by exposing one URL for all sources. |
