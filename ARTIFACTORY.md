
# Artifactory

During the software build process, developers produce various `artifacts` such as libraries, packages, binaries, and container images that are essential for application deployment and runtime. `Artifactory` is a universal **repository manager** that provides a centralized platform for storing, managing, and distributing these artifacts in a secure and efficient manner. Here are some of the use cases of an Artifactory:

- **CI/CD Integration**: In CI/CD, code is built and tested automatically. Artifactory acts as a central place to store the build outputs (like `.jar`, `.deb`, `.whl`, or Docker images). These artifacts can then be promoted across environments (dev → test → prod) without rebuilding, improving reliability and consistency.

- **Version Control for Binaries**: Artifactory keeps multiple versions of the same artifact, so teams can go back to previous builds if needed. This is essential for debugging, rollback, or recreating old environments.

- **Dependency Caching**: When projects rely on external libraries, Artifactory can cache these downloads locally. This speeds up builds and protects against outages if public repositories go down or get slow.

Over the years, dozens artifact repository managers have been developed to support software teams in managing and distributing build artifacts efficiently. These tools vary in capabilities, package format support, and deployment models ranging from self-hosted solutions to fully managed cloud-native services.

| Tool                          | Initial Release | Description                                                                                                                                     |
|-------------------------------|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| **Apache Archiva**            | 2007            | One of the earliest repository managers, focused on managing Maven artifacts. Lightweight and open-source, suitable for Java-centric workflows. |
| **Sonatype Nexus Repository** | 2008            | A widely used artifact repository manager that supports multiple formats (Maven, npm, Docker, etc.). Comes in OSS and Pro editions.             |
| **JFrog Artifactory**         | 2009            | A universal artifact manager supporting 30+ formats. Known for deep CI/CD integrations, multi-site replication, and enterprise-grade features.  |
| **Cloudsmith**                | 2017            | Fully managed cloud-native artifact repository supporting multiple formats (Docker, npm, Python, RubyGems, etc.). Offers global distribution.   |
| **Azure Artifacts**           | 2018            | Part of Azure DevOps. Supports Maven, npm, NuGet, and Python. Provides scoped feeds and tight integration with Azure CI/CD tools.               |
| **GitHub Packages**           | 2019            | GitHub’s artifact storage service for Docker, npm, RubyGems, NuGet, and more. Integrated tightly with GitHub Actions.                           |
| **GitLab Package Registry**   | 2019            | GitLab’s integrated package manager supporting Docker, Maven, npm, Conan, etc., directly within GitLab pipelines.                               |
| **AWS CodeArtifact**          | 2020            | Managed artifact repository service by AWS. Supports Maven, npm, PyPI, and NuGet. Integrated with IAM and AWS ecosystem.                        |
| **Google Artifact Registry**  | 2021            | A unified artifact storage solution in Google Cloud for Docker images, Maven, npm, and more. Replaces Google Container Registry (GCR).          |

## JFrog Artifactory

JFrog Artifactory is one of the most widely adopted and feature-rich artifact repository managers in the industry. It is available in multiple editions including a free open-source version and commercial editions catering to teams of all sizes, from individual developers to large-scale enterprises. Artifactory serves as a universal hub for managing artifacts across the software development lifecycle and supports deep integration with DevOps ecosystems. JFrog Artifactory supports more than 30 package types making it truly universal. It enables organizations to manage all their binaries from a single platform, regardless of technology stack.

- Build Tools: `Maven`, `Gradle`, `Ivy`, `SBT`
- Package Managers (programming):
    - JavaScript: `npm`, `Bower`
    - Python: `PyPI`, `Conda`
    - .NET: `NuGet`
    - Ruby: `RubyGems`, `CocoaPods`
    - C/C++: `Conan`
    - Go: `Go`
    - Rust: `Cargo`
    - R: `CRAN`
    - PHP: `Composer`
    - Dart: `Pub`
    - Swift: `Swift`
- Package Managers (Linux): `debian`, `rpm`, `opkg`
- Configuration Management: `Ansible`, `Chef`, `Puppet`
- Container and Orchestration: `Docker`, `OCI`, `Terraform`, `Helm`
- VM Provisioning: `Vagrant`
- Large File Storage for Git: `GitLFS`

A `repository` in Artifactory is a structured storage location used to manage and serve software artifacts throughout the development lifecycle. Repositories enable versioned artifact storage, enforce access control and security policies, and enable artifact retrieval and deployment for both developers and automated CI/CD pipelines. Artifactory supports several repository types, each serving a distinct purpose:

- **Local Repository**: Stores artifacts that are deployed directly to the Artifactory server by internal teams or build systems. Local repositories are typically used to host proprietary packages and internal build outputs.

- **Remote Repository**: Acts as a caching proxy for external repositories (e.g., PyPI, Maven Central, Docker Hub). When an artifact is requested, Artifactory fetches it from the upstream source, caches it locally, and serves subsequent requests from the cache.

- **Virtual Repository**: Aggregates multiple repositories (both local and remote) into a single, unified endpoint. Virtual repositories simplify client configuration by exposing a consolidated view of artifacts while applying consistent policies across multiple sources.
