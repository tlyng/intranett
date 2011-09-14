def allow_anonymous_robotstxt():
    from iw.rejectanonymous import addValidIds, addValidSubparts
    addValidIds('robots.txt')
    addValidIds('logged_out')
    addValidSubparts('portal_kss')


def allow_anonymous_activation():
    from iw.rejectanonymous import addValidIds, addValidSubparts
    addValidIds('activate_form')
    addValidSubparts('activate')


def allow_anonymous_invitation():
    from iw.rejectanonymous import addValidIds, addValidSubparts
    addValidIds('accept')


def optimize_rr_packing():
    from Products.ResourceRegistries.tools import CSSRegistry
    from Products.ResourceRegistries.tools import JSRegistry
    from Products.ResourceRegistries.tools import KSSRegistry
    from .compress import css, js
    CSSRegistry.CSSRegistryTool._compressCSS = css
    JSRegistry.JSRegistryTool._compressJS = js
    KSSRegistry.KSSRegistryTool._compressKSS = css


def apply():
    allow_anonymous_robotstxt()
    allow_anonymous_activation()
    allow_anonymous_invitation()
    optimize_rr_packing()
