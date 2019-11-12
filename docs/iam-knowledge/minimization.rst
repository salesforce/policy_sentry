
Minimization
---------------------------------------

This document explains the approach in the file titled ``policy_sentry/shared/minimize.py``\ , which is heavily borrowed from Netflix's `policyuniverse <https://github.com/Netflix-Skunkworks/policyuniverse/>`_ 

IAM Policies have character limits, which apply to individual policies, and there are also limits on the total aggregate policy sizes. As such, it is not possible to use exhaustive list of explicit IAM actions. To have granular control of specific IAM policies, we must use wildcards on IAM Actions, only in a programmatic manner. 

This is typically performed by humans by reducing policies to ``s3:Get*``\ , ``ec2:Describe*``\ , and other approaches of the sort. 

Netflix's PolicyUniverse\ `1 <https://github.com/Netflix-Skunkworks/policyuniverse/>`_ has addressed this problem using a few functions that we borrowed directly, and slightly modified. All of these functions are inside the aforementioned ``minimize.py`` file, and are also listed below:


* `get_denied_prefixes_from_desired <https://github.com/Netflix-Skunkworks/policyuniverse/blob/master/policyuniverse/expander_minimizer.py#L101>`_
* `check_min_permission_length <https://github.com/Netflix-Skunkworks/policyuniverse/blob/master/policyuniverse/expander_minimizer.py#L111>`_
* `minimize_statement_actions <https://github.com/Netflix-Skunkworks/policyuniverse/blob/master/policyuniverse/expander_minimizer.py#L123>`_

We modified the functions, in short, because of how we source our list of IAM actions. Policyuniverse leverages a file titled ``data.json``\ , which appears to be a manually altered version of the `policies.js <https://awspolicygen.s3.amazonaws.com/js/policies.js>`_ file included as part of the `AWS Policy Generator website <https://awspolicygen.s3.amazonaws.com/policygen.html>`_. However, that page is not updated as frequently. It also does not include the same details that we get from the `Actions, Resources, and Condition Keys page <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html>`_\ , like the Dependent Actions Field, service-specific conditions, and most importantly the multiple ARN format types that can apply to any particular IAM Action.

See the AWS IAM FAQ page for supporting details on IAM Size. For your convenience, the relevant text is clipped below.

..

   Q: How many policies can I attach to an IAM role?


   * For inline policies: You can add as many inline policies as you want to a user, role, or group, but
     the total aggregate policy size (the sum size of all inline policies) per entity cannot exceed the following limits:

     * User policy size cannot exceed 2,048 characters.
     * Role policy size cannot exceed 10,240 characters.
     * Group policy size cannot exceed 5,120 characters.

   * For managed policies: You can add up to 10 managed policies to a user, role, or group. 
   * The size of each managed policy cannot exceed 6,144 characters.

