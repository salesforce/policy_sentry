# Introduction


## Overview

Writing security-conscious IAM Policies by hand can be very tedious and inefficient. Many Infrastructure as Code developers have experienced something like this:

 * Determined to make your best effort to give users and roles the least amount of privilege you need to perform your duties, you spend way too much time combing through the AWS IAM Documentation on [Actions, Resources, and Condition Keys for AWS Services][1].
 * Your team lead encourages you to build security into your IAM Policies for product quality, but eventually you get frustrated due to project deadlines.
 * You don't have an embedded security person on your team who can write those IAM Policies for you, and there's no automated tool that will automagically sense the AWS API calls that you perform and then write them for you with Resource ARN constraints.
 * After fantasizing about that level of automation, you realize that writing least privilege IAM Policies, seemingly out of charity, will jeopardize your ability to finish your code in time to meet project deadlines.
 * You use Managed Policies (because hey, why not) or you eyeball the names of the API calls and use wildcards instead so you can move on with your life.

Such a process is not ideal for security or for Infrastructure as Code developers. We need to make it easier to write IAM Policies securely and abstract the complexity of writing least-privilege IAM policies. That's why I made this tool.

Policy Sentry allows users to create least-privilege IAM policies in a matter of seconds, rather than tediously writing IAM policies by hand. These policies are scoped down according to access levels and resources. In the case of a breach, this helps to limit the blast radius of compromised credentials by only giving IAM principals access to what they need.

**Before this tool, it could take hours to craft an IAM Policy with resource ARN constraints — but now it can take a matter of seconds**. This way, developers only have to determine the resources that they need to access, and **Policy Sentry abstracts the complexity of IAM policies** away from their development processes.

### Writing Secure Policies based on Resource Constraints and Access Levels

Policy Sentry's flagship feature is that it can create IAM policies based on resource ARNs and access levels. Our CRUD functionality takes the opinionated approach that IAC developers shouldn't have to understand the complexities of AWS IAM - we should abstract the complexity for them. In fact, developers should just be able to say...

* "I need Read/Write/List access to `arn:aws:s3:::example-org-sbx-vmimport`"
* "I need Permissions Management access to `arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret`"
* "I need Tagging access to `arn:aws:ssm:us-east-1:123456789012:parameter/test`"

...and our automation should create policies that correspond to those access levels.

How do we accomplish this? Well, Policy Sentry leverages the AWS documentation on [Actions, Resources, and Condition Keys][1] documentation to look up the actions, access levels, and resource types, and generates policies according to the ARNs and access levels. Consider the table snippet below:

<table class="tg">
  <tr>
    <th class="tg-fymr"><b>Actions</b></th>
    <th class="tg-fymr"><b>Access Level</b></th>
    <th class="tg-fymr"><b>Resource Types</b></th>
  </tr>
  <tr>
    <td class="tg-0pky"><code>ssm:GetParameter</code></td>
    <td class="tg-0pky">Read</td>
    <td class="tg-0pky">parameter</td>
  </tr>
  <tr>
    <td class="tg-0pky"><code>ssm:DescribeParameters</code></td>
    <td class="tg-0pky">List</td>
    <td class="tg-0pky">parameter</td>
  </tr>
  <tr>
    <td class="tg-0pky"><code>ssm:PutParameter</code></td>
    <td class="tg-0pky">Write</td>
    <td class="tg-0pky">parameter</td>
  </tr>
  <tr>
    <td class="tg-0pky"><code>secretsmanager:PutResourcePolicy</code></td>
    <td class="tg-0pky">Permissions management</td>
    <td class="tg-0pky">secret</td>
  </tr>
  <tr>
    <td class="tg-0pky"><code>secretsmanager:TagResource</code></td>
    <td class="tg-0pky">Tagging</td>
    <td class="tg-0pky">secret</td>
  </tr>
</table>

Policy Sentry aggregates all of that documentation into a single database and uses that database to generate policies according to actions, resources, and access levels.

[1]: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html
