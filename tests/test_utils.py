from lib.utils import email_to_department

def test_email_to_department():
    assert email_to_department('adam.smith@google.gov.uk') == 'google'
    assert email_to_department('adam.smith2@google.gov.uk') == 'google'
    assert email_to_department('adam.smith-gates@google.gov.uk') == 'google'
    assert email_to_department('fred@google.gov.uk') == 'google'
    assert email_to_department('fred@google.uk') == 'google'
    assert email_to_department('fred@google.ac.uk') == 'google'
    assert email_to_department('fred@google_.ac.uk') == 'google_'
    assert email_to_department('fred@GOOGLE.ac.uk') == 'google'
    assert email_to_department('fred@Google.ac.uk') == 'google'
    assert email_to_department('fred@GoOgLe.ac.uk') == 'google'
    assert email_to_department('fred@google10.ac.uk') == 'google10'