package app.pythonpractice;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

/**
 * Shows the web app that is packed inside the APK (assets/www). Nothing is loaded from the
 * internet except the Claude API calls the app itself makes for Hint / Explain.
 */
public class MainActivity extends Activity {
    // Requests to this host never leave the phone: they are answered from the APK's assets.
    private static final String HOST = "appassets.androidplatform.net";
    private static final Map<String, String> TYPES = new HashMap<>();

    static {
        TYPES.put("html", "text/html");
        TYPES.put("js", "text/javascript");
        TYPES.put("mjs", "text/javascript");
        TYPES.put("json", "application/json");
        TYPES.put("webmanifest", "application/manifest+json");
        TYPES.put("py", "text/plain");
        TYPES.put("svg", "image/svg+xml");
        TYPES.put("png", "image/png");
        TYPES.put("wasm", "application/wasm");
        TYPES.put("zip", "application/zip");
    }

    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true); // progress, code and settings live in localStorage

        webView.setWebChromeClient(new WebChromeClient()); // enables confirm() dialogs
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                Uri url = request.getUrl();
                if (!HOST.equals(url.getHost())) return null; // e.g. api.anthropic.com goes to the network
                String path = url.getPath();
                if (path == null || path.isEmpty() || path.equals("/")) path = "/index.html";
                String ext = path.substring(path.lastIndexOf('.') + 1);
                String type = TYPES.containsKey(ext) ? TYPES.get(ext) : "application/octet-stream";
                boolean text = type.startsWith("text/") || type.contains("json") || type.contains("svg");
                Map<String, String> headers = new HashMap<>();
                headers.put("Cache-Control", "no-cache");
                try {
                    InputStream in = getAssets().open("www" + path);
                    return new WebResourceResponse(type, text ? "utf-8" : null, 200, "OK", headers, in);
                } catch (IOException e) {
                    return new WebResourceResponse("text/plain", "utf-8", 404, "Not Found", headers,
                            new ByteArrayInputStream(new byte[0]));
                }
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                if (HOST.equals(request.getUrl().getHost())) return false;
                startActivity(new Intent(Intent.ACTION_VIEW, request.getUrl())); // outside links open in the browser
                return true;
            }
        });

        webView.loadUrl("https://" + HOST + "/index.html");
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) webView.goBack(); // exercise -> list
        else super.onBackPressed();
    }
}
